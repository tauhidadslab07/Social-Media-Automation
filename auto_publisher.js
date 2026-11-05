const fs = require('fs');
const https = require('https');
const path = require('path');

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

async function postFacebook(imagePath, caption) {
  const boundary = "----WebKitFormBoundary" + Math.random().toString(36).substring(2);
  const imageBuffer = fs.readFileSync(imagePath);

  let postData = [];
  postData.push(Buffer.from(`--${boundary}\r\nContent-Disposition: form-data; name="caption"\r\n\r\n${caption}\r\n`));
  postData.push(Buffer.from(`--${boundary}\r\nContent-Disposition: form-data; name="access_token"\r\n\r\n${pageToken}\r\n`));
  postData.push(Buffer.from(`--${boundary}\r\nContent-Disposition: form-data; name="source"; filename="poster.jpg"\r\nContent-Type: image/jpeg\r\n\r\n`));
  postData.push(imageBuffer);
  postData.push(Buffer.from(`\r\n--${boundary}--\r\n`));

  const body = Buffer.concat(postData);

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
  throw new Error(`Facebook failed: ${JSON.stringify(data)}`);
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

module.exports = { postFacebook, postLinkedIn };
