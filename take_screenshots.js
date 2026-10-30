const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const CHROME = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const htmlSource = fs.readFileSync(path.join(__dirname, 'preview_carousel.html'), 'utf8');

function makeSlideHtml(slideId) {
  return htmlSource.replace(
    '</body>',
    `<style>.slide-container:not(#${slideId}) { display: none !important; } .slide-container { margin-top: 0 !important; width: 1080px !important; height: 1350px !important; }</style></body>`
  );
}

fs.writeFileSync(path.join(__dirname, 'temp_slide1.html'), makeSlideHtml('slide-1'), 'utf8');
fs.writeFileSync(path.join(__dirname, 'temp_slide2.html'), makeSlideHtml('slide-2'), 'utf8');
fs.writeFileSync(path.join(__dirname, 'temp_slide7.html'), makeSlideHtml('slide-7'), 'utf8');

const s1Path = path.resolve(__dirname, 'temp_slide1.html').replace(/\\/g, '/');
const s2Path = path.resolve(__dirname, 'temp_slide2.html').replace(/\\/g, '/');
const s7Path = path.resolve(__dirname, 'temp_slide7.html').replace(/\\/g, '/');

const out1 = path.resolve(__dirname, 'carousel_preview_cover.png');
const out2 = path.resolve(__dirname, 'carousel_preview_step.png');
const out7 = path.resolve(__dirname, 'carousel_preview_outro.png');

console.log('Rendering Cover Slide (Slide 1)...');
execSync(`"${CHROME}" --headless=new --screenshot="${out1}" --window-size=1080,1350 --hide-scrollbars --virtual-time-budget=3000 "file:///${s1Path}"`);

console.log('Rendering Step Slide (Slide 2)...');
execSync(`"${CHROME}" --headless=new --screenshot="${out2}" --window-size=1080,1350 --hide-scrollbars --virtual-time-budget=3000 "file:///${s2Path}"`);

console.log('Rendering Outro Slide (Slide 7)...');
execSync(`"${CHROME}" --headless=new --screenshot="${out7}" --window-size=1080,1350 --hide-scrollbars --virtual-time-budget=3000 "file:///${s7Path}"`);

console.log('Screenshots completed successfully!');
