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

const token = process.env.LINKEDIN_ACCESS_TOKEN;
const author = process.env.LINKEDIN_AUTHOR_URN || "urn:li:person:1AdMFsDmDj";
const imagePath = "C:/Users/HP/.gemini/antigravity/brain/0d49db28-ded0-4a58-87ae-2e8a192c86ba/tauhidul_lego_poster_v3_1793360620777.jpg";

const caption = `A LEGO brick manufactured in 1958 still snaps perfectly into a LEGO brick made in 2026.

Think about the depth of that design decision:

In the last 68 years:
• Technology has fundamentally reshaped human existence.
• Thousands of toy companies went bankrupt trying to chase trends.
• Entire industries rose, dominated, and became obsolete.

Yet, LEGO never changed its fundamental locking mechanism.

Why? 
Because true innovation isn't about constantly breaking the foundation. It’s about building infinite new possibilities ON TOP OF a solid core.

In business and brand strategy, the most dangerous distraction is "novelty bias"—the urge to change what is already working simply because we are bored of it:
— Redesigning logos every year without strategic reason.
— Abandoning proven value propositions to chase short-term hype.
— Confusing motion with progress.

The strongest brands in the world don’t survive by reinventing themselves every quarter. 
They survive through backward-compatible consistency.

Master the fundamentals. 
Protect what works. 
Build everything else around it.

What is one timeless fundamental in your industry that technology will never replace?

---
#BrandStrategy #DesignThinking #Leadership #TimelessPrinciples #BusinessPhilosophy`;

async function main() {
  console.log("Publishing Day 1 to LinkedIn for Author:", author);

  // Step 1: Register Upload
  const regPayload = {
    registerUploadRequest: {
      recipes: ["urn:li:digitalmediaRecipe:feedshare-image"],
      owner: author,
      serviceRelationships: [{
        relationshipType: "OWNER",
        identifier: "urn:li:userGeneratedContent"
      }]
    }
  };

  const regRes = await fetch("https://api.linkedin.com/v2/assets?action=registerUpload", {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${token}`,
      "X-Restli-Protocol-Version": "2.0.0",
      "Content-Type": "application/json"
    },
    body: JSON.stringify(regPayload)
  });

  const regData = await regRes.json();
  if (!regRes.ok) {
    console.error("Register upload failed:", regRes.status, regData);
    return;
  }

  const uploadUrl = regData.value.uploadMechanism["com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"].uploadUrl;
  const assetUrn = regData.value.asset;
  console.log("Asset registered:", assetUrn);

  // Step 2: Upload image binary
  const fileBytes = fs.readFileSync(imagePath);
  const upRes = await fetch(uploadUrl, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${token}`,
      "Content-Type": "image/jpeg"
    },
    body: fileBytes
  });
  console.log("Binary upload status:", upRes.status);

  // Step 3: Create UGC Post
  const postPayload = {
    author: author,
    lifecycleState: "PUBLISHED",
    specificContent: {
      "com.linkedin.ugc.ShareContent": {
        shareCommentary: { text: caption },
        shareMediaCategory: "IMAGE",
        media: [{
          status: "READY",
          description: { text: "Timeless Principles: The LEGO Brick" },
          media: assetUrn,
          title: { text: "Consistency is the ultimate competitive advantage" }
        }]
      }
    },
    visibility: {
      "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
    }
  };

  const postRes = await fetch("https://api.linkedin.com/v2/ugcPosts", {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${token}`,
      "X-Restli-Protocol-Version": "2.0.0",
      "Content-Type": "application/json"
    },
    body: JSON.stringify(postPayload)
  });

  const postData = await postRes.json();
  console.log("Post status:", postRes.status);
  console.log("Post response:", JSON.stringify(postData, null, 2));

  if (postRes.ok) {
    console.log("\n🎉 SUCCESS! Day 1 is LIVE on LinkedIn!");
    console.log("Post ID:", postData.id);
  }
}

main().catch(console.error);
