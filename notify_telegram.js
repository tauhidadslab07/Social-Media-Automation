const fs = require('fs');
const path = require('path');
const dns = require('dns');

try {
  dns.setDefaultResultOrder('ipv4first');
} catch {}

const BOT_TOKEN = process.env.TELEGRAM_BOT_TOKEN || '9160899537:AAEfztioL4NVG8c_RRUHYscLCcBGK2kAVIA';
const CHAT_ID = process.env.TELEGRAM_CHAT_ID || '6096642555';

async function sendTelegramAlert() {
  if (!CHAT_ID) {
    console.log('[Telegram] No TELEGRAM_CHAT_ID provided. Skipping alert.');
    return;
  }

  const statePath = path.join(__dirname, 'published_state.json');
  if (!fs.existsSync(statePath)) {
    console.log('[Telegram] published_state.json not found.');
    return;
  }

  const state = JSON.parse(fs.readFileSync(statePath, 'utf8'));
  const history = state.history || [];
  const latest = history[history.length - 1];

  if (!latest) {
    console.log('[Telegram] No history records found.');
    return;
  }

  const isPublished = latest.status === 'PUBLISHED';
  const fbUrl = latest.facebook_post_id
    ? `https://www.facebook.com/1325501797313655/posts/${latest.facebook_post_id.replace('1325501797313655_', '')}`
    : 'N/A';
  const liUrl = latest.linkedin_post_id
    ? `https://www.linkedin.com/feed/update/${latest.linkedin_post_id}`
    : 'N/A';

  let message = '';
  if (isPublished) {
    message = `🔔 <b>Daily Social Media Post Live!</b>\n\n` +
      `📅 <b>Date:</b> ${latest.date}\n` +
      `📌 <b>Day ${latest.day}:</b> ${latest.item}\n` +
      `⚡ <b>Status:</b> 🟢 <b>PUBLISHED</b>\n\n` +
      `🔗 <b>Live Post Links:</b>\n` +
      `📘 <a href="${fbUrl}">Facebook Post</a>\n` +
      `💼 <a href="${liUrl}">LinkedIn Post</a>\n\n` +
      `<i>Automated via Tauhid Ads Lab Cloud Runner</i>`;
  } else {
    message = `⚠️ <b>ALERT: Daily Social Post Failed!</b>\n\n` +
      `📅 <b>Date:</b> ${latest.date}\n` +
      `📌 <b>Day ${latest.day}:</b> ${latest.item}\n` +
      `⚡ <b>Status:</b> 🔴 <b>FAILED</b>\n\n` +
      `❌ <b>Error:</b> <code>${latest.error || 'Unknown failure'}</code>\n\n` +
      `<i>Please check your tokens or network connection.</i>`;
  }

  const payload = {
    chat_id: CHAT_ID,
    text: message,
    parse_mode: 'HTML',
    disable_web_page_preview: false,
  };

  try {
    const res = await fetch(`https://api.telegram.org/bot${BOT_TOKEN}/sendMessage`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    const result = await res.json();
    console.log('[Telegram] Notification sent result:', result.ok ? 'SUCCESS' : result);
  } catch (err) {
    console.error('[Telegram] Failed to send notification:', err.message);
  }
}

if (require.main === module) {
  sendTelegramAlert().catch(console.error);
}

module.exports = { sendTelegramAlert };
