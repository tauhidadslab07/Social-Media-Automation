const fs = require('fs');
const path = require('path');
const { postFacebook, postLinkedIn } = require('./auto_publisher');

async function runDailyPost() {
  console.log("=== RUNNING DAILY AUTOMATED POST ===");
  const statePath = path.join(__dirname, 'published_state.json');
  const topicsPath = path.join(__dirname, 'topics_timeless_60days.json');

  if (!fs.existsSync(statePath) || !fs.existsSync(topicsPath)) {
    console.error("Missing state or topics file!");
    return;
  }

  const state = JSON.parse(fs.readFileSync(statePath, 'utf8'));
  const topics = JSON.parse(fs.readFileSync(topicsPath, 'utf8'));

  // Safety Check: Check if a post was already published today
  const todayStr = new Date().toISOString().split('T')[0];
  const lastHistory = state.history[state.history.length - 1];
  if (lastHistory && lastHistory.date === todayStr && lastHistory.status === 'PUBLISHED') {
    console.log(`[Scheduler] Today's post (Day ${lastHistory.day}: ${lastHistory.item}) was already published today (${todayStr}).`);
    console.log("[Scheduler] Skipping run. Next post will trigger tomorrow.");
    return;
  }

  const nextDayIndex = state.current_day; // current_day=2 means index 2 (Day 3)
  if (nextDayIndex >= topics.length) {
    console.log("All 60 days have been published!");
    return;
  }

  const topic = topics[nextDayIndex];
  console.log(`Processing Day ${topic.day}: ${topic.item} (${topic.headline})`);

  // Designate image path for Day N
  let imagePath = path.join(__dirname, `day_${topic.day}_poster.jpg`);
  if (topic.day === 3) {
    const customDay3 = path.join(__dirname, 'tauhidul_bic_pen_poster.jpg');
    if (fs.existsSync(customDay3)) imagePath = customDay3;
  }

  if (!fs.existsSync(imagePath)) {
    console.log(`Warning: Image for Day ${topic.day} not found at ${imagePath}. Checking fallback.`);
    const fallbackPath = "C:/Users/HP/.gemini/antigravity/brain/0d49db28-ded0-4a58-87ae-2e8a192c86ba/tauhidul_lego_poster_v3_1793360620777.jpg";
    if (fs.existsSync(fallbackPath)) imagePath = fallbackPath;
  }

  let caption = "";
  if (topic.day === 3) {
    caption = `In 1950, Marcel Bich launched a simple clear plastic ballpoint pen with a blue cap.

Today, in 2026, the BIC Cristal looks virtually identical.
Over 100,000,000,000 pens sold. It even sits in the permanent collection of the Museum of Modern Art (MoMA) in New York.

Think about why it survived seven decades of technological disruption:
• No digital apps.
• No Bluetooth connectivity.
• No feature bloat.

It solves exactly ONE problem with radical simplicity: putting ink on paper smoothly, reliably, and effortlessly.

In business and marketing, we often fall into the trap of "Feature Creep":
— Over-complicating user onboarding.
— Adding 15 unnecessary features that dilute the core value proposition.
— Designing 7-step funnels when a 2-step conversation converts 3x better.

Radical simplicity is the ultimate sophistication.

Remove the friction. Strip away the noise. Make your core solution undeniable.

What is one unnecessary complexity in your business that you can eliminate today?

---
#ProductStrategy #DesignThinking #Simplicity #Leadership #TimelessPrinciples #BrandStrategy`;
  } else if (topic.day === 4) {
    caption = `In 1953, a small three-person team in San Diego set out to create a rust-prevention solvent.

They failed on attempt 1.
They failed on attempt 10.
They failed on attempt 39.

On the 40th attempt, the formula worked: Water Displacement, 40th formula (WD-40).

Over 73 years later, that exact same formula is in 4 out of 5 American households and trusted across the globe.

Here is the greatest business lesson WD-40 teaches us:
They never diluted their identity.
They didn’t launch 50 random product lines.
They didn’t try to be everything to everyone.

They owned ONE universal problem—preventing rust, displacing moisture, and freeing stuck mechanisms—and solved it better than anyone else on earth.

In modern growth strategy, the biggest mistake agencies and brands make is horizontal distraction:
— Launching 10 half-baked services instead of dominating one core offer.
— Confusing product breadth with enterprise value.
— Abandoning category ownership in search of quick, shiny revenue.

Dominance doesn’t come from solving 100 problems mediocrely.
It comes from solving ONE critical problem so permanently that your brand name becomes the noun.

What is the single core problem your business owns?

---
#CategoryDesign #BrandPositioning #Leadership #TimelessPrinciples #BusinessStrategy #Growth`;
  } else {
    caption = `${topic.item} (${topic.year})

${topic.headline}.

${topic.concept}

In modern business and marketing, the greatest risk is constantly disrupting what already works.
Master the core fundamentals. Protect your foundation. Build everything else on top.

What is one fundamental principle in your work that will NEVER change?

---
#BrandStrategy #TimelessPrinciples #Leadership #DesignThinking #BusinessPhilosophy`;
  }

  console.log(`Publishing Day ${topic.day} to Facebook...`);
  const fbPostId = await postFacebook(imagePath, caption);
  console.log(`Facebook Success! Post ID: ${fbPostId}`);

  console.log(`Publishing Day ${topic.day} to LinkedIn...`);
  const liPostId = await postLinkedIn(imagePath, caption, topic.headline);
  console.log(`LinkedIn Success! Post ID: ${liPostId}`);

  // Update state
  state.current_day = topic.day;
  state.history.push({
    day: topic.day,
    date: new Date().toISOString().split('T')[0],
    item: topic.item,
    facebook_post_id: fbPostId,
    linkedin_post_id: liPostId,
    status: 'PUBLISHED'
  });

  fs.writeFileSync(statePath, JSON.stringify(state, null, 2));
  console.log(`State updated. Day ${topic.day} recorded successfully!`);
}

module.exports = { runDailyPost };

if (require.main === module) {
  runDailyPost().catch(console.error);
}
