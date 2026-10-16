# 🚀 Automated Social Media Poster & Designer

সম্পূর্ণ ফ্রি এবং ১০০% অটোমেটেড সোশ্যাল মিডিয়া সিস্টেম। প্রতিদিন ৪টি করে ব্র‍্যান্ডেড গ্রাফিক্স ডিজাইন হবে এবং স্বয়ংক্রিয়ভাবে **Facebook Page**, **Instagram Business**, এবং **LinkedIn**-এ পাবলিশ হয়ে যাবে।

---

## 📂 ফাইল পরিচিতি

- [`content_engine.py`](content_engine.py): Gemini AI দিয়ে পোস্টের টপিক, টাইটেল, বাংলা/ইংরেজি ক্যাপশন ও হ্যাশট্যাগ তৈরি করে।
- [`image_engine.py`](image_engine.py): Python Pillow দিয়ে ১০৮০×১০৮০ স্কয়ার আধুনিক ব্র‍্যান্ডেড সোশ্যাল মিডিয়া ব্যানার ডিজাইন করে।
- [`social_poster.py`](social_poster.py): Facebook, Instagram এবং LinkedIn API হ্যান্ডলার।
- [`main.py`](main.py): প্রধান এক্সিকিউটর স্ক্রিপ্ট।
- [`.github/workflows/daily_post.yml`](.github/workflows/daily_post.yml): প্রতিদিন ৪ বার (সকাল ৯টা, দুপুর ১টা, বিকাল ৫টা, রাত ৯টা বাংলাদেশ সময়) ফ্রিতে স্বয়ংক্রিয়ভাবে চালানোর ক্লাউড ওয়ার্কফ্লো।

---

## 🔑 প্রয়োজনীয় API Keys ও ক্রেডেনশিয়ালস সংগ্রহ নির্দেশিকা

### ১. Google Gemini API Key (ফ্রি)
1. ভিজিট করুন: [Google AI Studio](https://aistudio.google.com/)
2. "Get API key" বাটনে ক্লিক করে একটি ফ্রি API Key কপি করুন।

### ২. ImgBB API Key (ইন্সটাগ্রামের ইমেজ হোস্টিংয়ের জন্য - ফ্রি)
*ইনস্টাগ্রাম Graph API-তে ছবি পোস্ট করতে হলে ছবিটির একটি পাবলিক লিংক লাগে।*
1. ভিজিট করুন: [ImgBB API](https://api.imgbb.com/)
2. লগইন করে "Get API Key"-এ ক্লিক করে কি-টি কপি করুন।

### ৩. Meta API (Facebook Page & Instagram Business)
1. [Meta for Developers](https://developers.facebook.com/)-এ যান এবং একটি App তৈরি করুন।
2. **Graph API Explorer** টুল থেকে আপনার Facebook Page-এর `Page Access Token` সংগ্রহ করুন।
3. পারমিশন যোগ করুন: `pages_manage_posts`, `pages_read_engagement`, `instagram_basic`, `instagram_content_publish`।
4. ফেসবুক পেজ সেটিংস থেকে আপনার **Page ID** এবং ইনস্টাগ্রাম অ্যাকাউন্টের **Instagram Account ID** নিন।

### ৪. LinkedIn API
1. [LinkedIn Developers](https://www.linkedin.com/developers/)-এ গিয়ে একটি অ্যাপ তৈরি করুন।
2. "Share on LinkedIn" প্রোডাক্ট সক্রিয় করুন।
3. OAuth 2.0 টোকেন জেনারেট করুন এবং আপনার পেজ বা প্রোফাইলের URN (যেমন: `urn:li:organization:12345678`) সংগ্রহ করুন।

---

## ⚙️ GitHub Actions-এ ক্লাউড সেটআপ (কম্পিউটার বন্ধ থাকলেও চলবে)

1. এই কোডগুলো আপনার GitHub অ্যাকাউন্টে একটি রিপোজিটরিতে (Private বা Public) পুশ/আপলোড করুন।
2. রিপোজিটরির **Settings > Secrets and variables > Actions**-এ যান।
3. **New repository secret**-এ ক্লিক করে নিচের নামগুলোতে আপনার ভ্যালুগুলো যোগ করুন:
   - `GEMINI_API_KEY`
   - `BRAND_NAME` (যেমন: আপনার পেজের নাম)
   - `BRAND_HANDLE` (যেমন: `@mybrand`)
   - `NICHE_TOPIC` (যেমন: `AI Tools, Tech Tips, Productivity`)
   - `FACEBOOK_PAGE_ID`
   - `FACEBOOK_PAGE_ACCESS_TOKEN`
   - `INSTAGRAM_ACCOUNT_ID`
   - `LINKEDIN_ACCESS_TOKEN`
   - `LINKEDIN_AUTHOR_URN`
   - `IMGBB_API_KEY`
4. এরপর **Actions** ট্যাবে গেলে দেখতে পাবেন `Automated Daily Social Media Poster` রেডি হয়ে গেছে। আপনি চাইলে যেকোনো সময় "Run workflow"-তে ক্লিক করে টেস্ট করতে পারেন!
