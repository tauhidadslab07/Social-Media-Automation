const fs = require('fs');
const https = require('https');
const path = require('path');
const dns = require('dns');

// Prioritize IPv4 to prevent IPv6 routing timeouts
if (dns.setDefaultResultOrder) {
  dns.setDefaultResultOrder('ipv4first');
}

function loadEnv() {
  const envPath = path.join(__dirname, '.env');
  if (fs.existsSync(envPath)) {
    const lines = fs.readFileSync(envPath, 'utf8').split('\n');
    for (const line of lines) {
      const trimmed = line.trim();
      if (!trimmed || trimmed.startsWith('#')) continue;
      const idx = trimmed.indexOf('=');
      if (idx !== -1) {
        process.env[trimmed.slice(0, idx).trim()] = trimmed.slice(idx + 1).trim();
      }
    }
  }
}
loadEnv();

const pageId = process.env.FACEBOOK_PAGE_ID || "1325501797313655";
const pageToken = process.env.FACEBOOK_PAGE_ACCESS_TOKEN;
const liToken = process.env.LINKEDIN_ACCESS_TOKEN;
const liAuthor = process.env.LINKEDIN_AUTHOR_URN || "urn:li:person:1AdMFsDmDj";

async function postFacebook(imagePath, caption, retries = 3) {
  const boundary = "----WebKitFormBoundary" + Math.random().toString(36).substring(2);
  const imageBuffer = fs.readFileSync(imagePath);

  let postData = [];
  postData.push(Buffer.from(`--${boundary}\r\nContent-Disposition: form-data; name="caption"\r\n\r\n${caption}\r\n`));
  postData.push(Buffer.from(`--${boundary}\r\nContent-Disposition: form-data; name="access_token"\r\n\r\n${pageToken}\r\n`));
  postData.push(Buffer.from(`--${boundary}\r\nContent-Disposition: form-data; name="source"; filename="poster.jpg"\r\nContent-Type: image/jpeg\r\n\r\n`));
  postData.push(imageBuffer);
  postData.push(Buffer.from(`\r\n--${boundary}--\r\n`));

  const body = Buffer.concat(postData);

  for (let attempt = 1; attempt <= retries; attempt++) {
    try {
      const res = await fetch(`https://graph.facebook.com/v19.0/${pageId}/photos`, {
        method: 'POST',
        headers: {
          'Content-Type': `multipart/form-data; boundary=${boundary}`,
          'Content-Length': body.length
        },
        body: body
      });

      const data = await res.json();
      if (res.ok && data.id) {
        return data.post_id || data.id;
      }
      throw new Error(`Facebook API error: ${JSON.stringify(data)}`);
    } catch (err) {
      console.warn(`[Facebook] Attempt ${attempt}/${retries} failed: ${err.message}`);
      if (attempt < retries) {
        console.log(`[Facebook] Retrying in 5 seconds...`);
        await new Promise(r => setTimeout(r, 5000));
      } else {
        throw err;
      }
    }
  }
}

async function postLinkedIn(imagePath, caption, title) {
  // Step 1: Register
  const regRes = await fetch("https://api.linkedin.com/v2/assets?action=registerUpload", {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${liToken}`,
      "X-Restli-Protocol-Version": "2.0.0",
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      registerUploadRequest: {
        recipes: ["urn:li:digitalmediaRecipe:feedshare-image"],
        owner: liAuthor,
        serviceRelationships: [{ relationshipType: "OWNER", identifier: "urn:li:userGeneratedContent" }]
      }
    })
  });
  const regData = await regRes.json();
  if (!regRes.ok) throw new Error(`LinkedIn register failed: ${JSON.stringify(regData)}`);

  const uploadUrl = regData.value.uploadMechanism["com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"].uploadUrl;
  const assetUrn = regData.value.asset;

  // Step 2: Binary
  const bytes = fs.readFileSync(imagePath);
  await fetch(uploadUrl, {
    method: "POST",
    headers: { "Authorization": `Bearer ${liToken}`, "Content-Type": "image/jpeg" },
    body: bytes
  });

  // Step 3: UGC Post
  const postRes = await fetch("https://api.linkedin.com/v2/ugcPosts", {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${liToken}`,
      "X-Restli-Protocol-Version": "2.0.0",
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      author: liAuthor,
      lifecycleState: "PUBLISHED",
      specificContent: {
        "com.linkedin.ugc.ShareContent": {
          shareCommentary: { text: caption },
          shareMediaCategory: "IMAGE",
          media: [{
            status: "READY",
            description: { text: title },
            media: assetUrn,
            title: { text: title }
          }]
        }
      },
      visibility: { "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC" }
    })
  });

  const postData = await postRes.json();
  if (!postRes.ok) throw new Error(`LinkedIn post failed: ${JSON.stringify(postData)}`);
  return postData.id;
}

async function postLinkedInDocument(pdfPath, caption, title = "Server-Side Tracking Blueprint") {
  // Step 1: Initialize Document Upload
  const initRes = await fetch("https://api.linkedin.com/rest/documents?action=initializeUpload", {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${liToken}`,
      "X-Restli-Protocol-Version": "2.0.0",
      "Linkedin-Version": "202511",
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      initializeUploadRequest: {
        owner: liAuthor
      }
    })
  });
  const initData = await initRes.json();
  if (!initRes.ok) throw new Error(`LinkedIn Document init failed: ${JSON.stringify(initData)}`);

  const uploadUrl = initData.value.uploadUrl;
  const docUrn = initData.value.document;
  console.log(`[LinkedIn Document] Initialized successfully. Document URN: ${docUrn}`);

  // Step 2: Binary Upload via PUT
  const pdfBytes = fs.readFileSync(pdfPath);
  const upRes = await fetch(uploadUrl, {
    method: "PUT",
    headers: { "Content-Type": "application/pdf" },
    body: pdfBytes
  });
  if (!upRes.ok) throw new Error(`LinkedIn Document upload failed: ${upRes.statusText}`);
  console.log("[LinkedIn Document] PDF binary uploaded successfully.");

  // Step 3: Create Post via /rest/posts
  const postRes = await fetch("https://api.linkedin.com/rest/posts", {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${liToken}`,
      "X-Restli-Protocol-Version": "2.0.0",
      "Linkedin-Version": "202511",
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      author: liAuthor,
      commentary: caption,
      visibility: "PUBLIC",
      distribution: {
        feedDistribution: "MAIN_FEED",
        targetEntities: [],
        thirdPartyDistributionChannels: []
      },
      content: {
        media: {
          id: docUrn,
          title: title
        }
      },
      lifecycleState: "PUBLISHED",
      isReshareDisabledByAuthor: false
    })
  });

  if (!postRes.ok) {
    const errData = await postRes.text();
    throw new Error(`LinkedIn Document post failed: ${errData}`);
  }
  const postId = postRes.headers.get("x-restli-id") || "PUBLISHED";
  console.log(`[LinkedIn Native PDF Document] Successfully published! Post ID: ${postId}`);
  return postId;
}

module.exports = { postFacebook, postLinkedIn, postLinkedInDocument };
