const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const CHROME = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";

function renderBrandPost(postData, outputPath) {
  const portraitPath = path.join(__dirname, 'tauhid_portrait.jpg');
  let portraitDataUrl = '';
  if (fs.existsSync(portraitPath)) {
    const portraitBase64 = fs.readFileSync(portraitPath).toString('base64');
    portraitDataUrl = 'data:image/jpeg;base64,' + portraitBase64;
  }

  const badge = postData.badge || "STORE SPEED · HIGHER ROAS";
  const line1 = postData.graphic_title_line1 || "HEAVY PIXELS KILL CHECKOUTS";
  const line2 = postData.graphic_title_line2 || "CLEAN SPEED & RECOVER ROAS";
  const subtitle = postData.graphic_subtitle || "Stop losing 30% of mobile buyers to slow browser scripts. Move to a single sGTM cloud stream.";

  // Dynamic font size based on length
  const maxLen = Math.max(line1.length, line2.length);
  const headlineFontSize = maxLen <= 18 ? 58 : (maxLen <= 24 ? 52 : 48);

  const html = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap');
  
  * { box-sizing: border-box; margin: 0; padding: 0; }
  
  body {
    width: 1080px;
    height: 1080px;
    background: #060913;
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    position: relative;
    overflow: hidden;
    color: #FFFFFF;
  }

  /* Architectural Mesh & Radial Flares */
  .ambient-flare-cyan {
    position: absolute;
    top: -120px;
    left: -100px;
    width: 650px;
    height: 650px;
    background: radial-gradient(circle, rgba(56, 189, 248, 0.18) 0%, rgba(6, 9, 19, 0) 70%);
    pointer-events: none;
    z-index: 1;
  }

  .ambient-flare-green {
    position: absolute;
    bottom: 40px;
    right: -80px;
    width: 700px;
    height: 700px;
    background: radial-gradient(circle, rgba(34, 197, 94, 0.15) 0%, rgba(6, 9, 19, 0) 70%);
    pointer-events: none;
    z-index: 1;
  }

  /* Subtle High-Tech Dot Grid */
  .grid-pattern {
    position: absolute;
    inset: 0;
    background-image: radial-gradient(rgba(255, 255, 255, 0.08) 1px, transparent 1px);
    background-size: 36px 36px;
    opacity: 0.65;
    pointer-events: none;
    z-index: 2;
  }

  /* Header Container */
  .header {
    position: relative;
    z-index: 10;
    padding: 44px 54px 0 54px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .brand-logo-group {
    display: flex;
    align-items: center;
    gap: 14px;
  }

  .logo-icon {
    width: 44px;
    height: 44px;
    border-radius: 12px;
    background: linear-gradient(135deg, #0ea5e9 0%, #22c55e 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 0 20px rgba(56, 189, 248, 0.4);
    font-weight: 800;
    font-size: 20px;
    color: #FFFFFF;
    letter-spacing: -1px;
  }

  .brand-text-wrapper {
    display: flex;
    flex-direction: column;
  }

  .brand-name {
    font-size: 24px;
    font-weight: 800;
    letter-spacing: 0.5px;
    display: flex;
    align-items: center;
    gap: 6px;
  }

  .name-white { color: #FFFFFF; }
  .name-blue { color: #38BDF8; }
  .name-green { color: #22C55E; }

  .brand-tagline {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2px;
    color: #94A3B8;
    margin-top: 2px;
  }

  .live-status-pill {
    display: flex;
    align-items: center;
    gap: 8px;
    background: rgba(15, 23, 42, 0.85);
    border: 1px solid rgba(56, 189, 248, 0.3);
    padding: 8px 18px;
    border-radius: 9999px;
    font-size: 13px;
    font-weight: 700;
    color: #E2E8F0;
    backdrop-filter: blur(10px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  }

  .live-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #22C55E;
    box-shadow: 0 0 10px #22C55E;
  }

  /* Content Area (Topic Badge, Headline & Subheadline) */
  .content-area {
    position: relative;
    z-index: 10;
    padding: 24px 54px 0 54px;
  }

  .topic-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(14, 165, 233, 0.12);
    border: 1px solid rgba(56, 189, 248, 0.35);
    color: #38BDF8;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 1.5px;
    padding: 6px 18px;
    border-radius: 9999px;
    text-transform: uppercase;
    margin-bottom: 14px;
  }

  .headline {
    font-size: ${headlineFontSize}px;
    font-weight: 800;
    line-height: 1.15;
    letter-spacing: -0.5px;
    max-width: 980px;
    text-transform: uppercase;
  }

  .headline .text-white { 
    color: #FFFFFF; 
    display: block;
  }
  .headline .text-blue { 
    color: #38BDF8; 
    display: block;
  }

  .subhead {
    color: #CBD5E1;
    font-size: 24px;
    font-weight: 500;
    line-height: 1.42;
    margin-top: 14px;
    max-width: 880px;
    letter-spacing: 0.1px;
  }

  /* Studio Stage for Portrait */
  .portrait-stage {
    position: absolute;
    bottom: 96px;
    left: 50%;
    transform: translateX(-50%);
    width: 720px;
    height: 590px;
    z-index: 15;
    border-radius: 48px 48px 0 0;
    background: #0B1120;
    border: 2px solid rgba(56, 189, 248, 0.35);
    border-bottom: none;
    overflow: hidden;
    box-shadow: 0 -15px 45px rgba(0, 0, 0, 0.5), 0 0 50px rgba(56, 189, 248, 0.12);
  }

  .portrait-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center 10%;
    display: block;
  }

  /* Signature Bottom Conversion Dock */
  .bottom-dock {
    position: absolute;
    bottom: 28px;
    left: 54px;
    right: 54px;
    height: 76px;
    background: rgba(11, 17, 32, 0.95);
    border: 1.5px solid rgba(56, 189, 248, 0.35);
    border-radius: 22px;
    z-index: 30;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 16px 0 24px;
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.6), 0 0 25px rgba(34, 197, 94, 0.15);
    backdrop-filter: blur(16px);
  }

  .dock-left {
    display: flex;
    align-items: center;
    gap: 18px;
  }

  .dock-url {
    font-size: 19px;
    font-weight: 700;
    color: #FFFFFF;
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .dock-url span.accent {
    color: #38BDF8;
  }

  .dock-divider {
    color: #334155;
    font-size: 18px;
  }

  .dock-phone {
    font-size: 18px;
    font-weight: 700;
    color: #38BDF8;
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .dock-cta-btn {
    background: #22C55E;
    color: #060913;
    font-size: 17px;
    font-weight: 800;
    padding: 12px 24px;
    border-radius: 14px;
    display: flex;
    align-items: center;
    gap: 8px;
    box-shadow: 0 0 20px rgba(34, 197, 94, 0.45);
  }
</style>
</head>
<body>

  <div class="ambient-flare-cyan"></div>
  <div class="ambient-flare-green"></div>
  <div class="grid-pattern"></div>

  <!-- Header -->
  <div class="header">
    <div class="brand-logo-group">
      <div class="logo-icon">T</div>
      <div class="brand-text-wrapper">
        <div class="brand-name">
          <span class="name-white">TAUHID</span>
          <span class="name-blue">ADS</span>
          <span class="name-green">LAB</span>
        </div>
        <div class="brand-tagline">GOOGLE & META ADS + TRACKING</div>
      </div>
    </div>
    <div class="live-status-pill">
      <div class="live-dot"></div>
      <span>1:1 DATA RECONCILED</span>
    </div>
  </div>

  <!-- Content -->
  <div class="content-area">
    <div class="topic-pill">
      <span>● ${badge}</span>
    </div>
    <h1 class="headline">
      <span class="text-white">${line1}</span>
      <span class="text-blue">${line2}</span>
    </h1>
    <p class="subhead">
      ${subtitle}
    </p>
  </div>

  <!-- Portrait Stage -->
  <div class="portrait-stage">
    ${portraitDataUrl ? `<img class="portrait-img" src="${portraitDataUrl}" alt="Tauhid">` : ''}
  </div>

  <!-- Signature Bottom Dock -->
  <div class="bottom-dock">
    <div class="dock-left">
      <div class="dock-url">🌐 tauhidadslab<span class="accent">.com</span></div>
      <div class="dock-divider">|</div>
      <div class="dock-phone">💬 WhatsApp: +8801624608468</div>
    </div>
    <div class="dock-cta-btn">Book Audit →</div>
  </div>

</body>
</html>`;

  const tempHtmlPath = path.join(__dirname, 'temp_brand_render.html');
  fs.writeFileSync(tempHtmlPath, html, 'utf8');

  const htmlUrl = 'file:///' + path.resolve(tempHtmlPath).replace(/\\/g, '/');
  console.log(`Rendering graphic to ${outputPath}...`);
  execSync(`"${CHROME}" --headless=new --screenshot="${outputPath}" --window-size=1080,1080 --hide-scrollbars --virtual-time-budget=3000 "${htmlUrl}"`);
  console.log('Rendering complete!');

  try {
    fs.unlinkSync(tempHtmlPath);
  } catch (e) {}
  return outputPath;
}

// If run directly, render Day 5
if (require.main === module) {
  const day5Data = {
    badge: "STORE SPEED · HIGHER ROAS",
    graphic_title_line1: "HEAVY PIXELS KILL CHECKOUTS",
    graphic_title_line2: "CLEAN SPEED & RECOVER ROAS",
    graphic_subtitle: "Stop losing 30% of mobile buyers to slow browser scripts. Move to a single sGTM cloud stream."
  };
  const out = path.join(__dirname, "tauhid_brand_optimized.png");
  renderBrandPost(day5Data, out);
}

module.exports = { renderBrandPost };
