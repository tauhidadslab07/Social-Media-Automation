const fs = require('fs');
const https = require('https');
const path = require('path');

// Simple .env parser without external dependencies
function loadEnv() {
  const envPath = path.join(__dirname, '.env');
  if (fs.existsSync(envPath)) {
    const lines = fs.readFileSync(envPath, 'utf8').split('\n');
    for (const line of lines) {
      const trimmed = line.trim();
      if (!trimmed || trimmed.startsWith('#')) continue;
      const idx = trimmed.indexOf('=');
      if (idx !== -1) {
        const key = trimmed.slice(0, idx).trim();
        const val = trimmed.slice(idx + 1).trim();
        process.env[key] = val;
      }
    }
  }
}
loadEnv();

const pageId = process.env.FACEBOOK_PAGE_ID || "1325501797313655";
const pageToken = process.env.FACEBOOK_PAGE_ACCESS_TOKEN;
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

const boundary = "----WebKitFormBoundary" + Math.random().toString(36).substring(2);
const imageBuffer = fs.readFileSync(imagePath);

let postData = [];
postData.push(Buffer.from(`--${boundary}\r\nContent-Disposition: form-data; name="caption"\r\n\r\n${caption}\r\n`));
postData.push(Buffer.from(`--${boundary}\r\nContent-Disposition: form-data; name="access_token"\r\n\r\n${pageToken}\r\n`));
postData.push(Buffer.from(`--${boundary}\r\nContent-Disposition: form-data; name="source"; filename="lego_poster.jpg"\r\nContent-Type: image/jpeg\r\n\r\n`));
postData.push(imageBuffer);
postData.push(Buffer.from(`\r\n--${boundary}--\r\n`));

const body = Buffer.concat(postData);

console.log("Publishing Day 1 to Facebook Page (Tauhid Ads Lab)...");

const req = https.request({
  hostname: 'graph.facebook.com',
  path: `/v19.0/${pageId}/photos`,
  method: 'POST',
  headers: {
    'Content-Type': `multipart/form-data; boundary=${boundary}`,
    'Content-Length': body.length
  }
}, res => {
  let responseText = '';
  res.on('data', chunk => responseText += chunk);
  res.on('end', () => {
    console.log('Status:', res.statusCode);
    console.log('Response:', responseText);
    try {
      const parsed = JSON.parse(responseText);
      if (parsed.id) {
        console.log('\n🎉 SUCCESS! Day 1 is LIVE on Facebook Page!');
        console.log('Photo ID:', parsed.id);
        console.log('Post ID:', parsed.post_id || parsed.id);
        console.log('Link: https://www.facebook.com/' + (parsed.post_id || parsed.id));
      }
    } catch(e) {}
  });
});

req.on('error', e => console.error('Error:', e));
req.write(body);
req.end();
