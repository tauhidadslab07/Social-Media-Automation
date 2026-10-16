import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

# Meta credentials
FB_PAGE_ID = os.getenv("FACEBOOK_PAGE_ID")
FB_PAGE_TOKEN = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN")
IG_ACCOUNT_ID = os.getenv("INSTAGRAM_ACCOUNT_ID")

# LinkedIn credentials
LI_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN")
LI_AUTHOR_URN = os.getenv("LINKEDIN_AUTHOR_URN")

# Image hosting for Instagram (ImgBB)
IMGBB_API_KEY = os.getenv("IMGBB_API_KEY")

def upload_image_to_imgbb(image_path):
    """
    Uploads the local graphic to ImgBB to obtain a public HTTPS URL.
    This is required by Instagram Graph API.
    """
    if not IMGBB_API_KEY:
        print("[ImgBB] Error: IMGBB_API_KEY is not set. Instagram requires a public image URL.")
        return None
        
    url = "https://api.imgbb.com/1/upload"
    try:
        with open(image_path, "rb") as file:
            payload = {"key": IMGBB_API_KEY}
            files = {"image": file}
            response = requests.post(url, data=payload, files=files, timeout=30)
            response.raise_for_status()
            res_json = response.json()
            image_url = res_json["data"]["url"]
            print(f"[ImgBB] Image uploaded successfully: {image_url}")
            return image_url
    except Exception as e:
        print(f"[ImgBB] Upload failed: {e}")
        return None

def post_to_facebook(image_path, caption):
    """
    Publishes an image post to Facebook Page.
    """
    if not FB_PAGE_ID or not FB_PAGE_TOKEN:
        print("[Facebook] Skipped: FB_PAGE_ID or FB_PAGE_ACCESS_TOKEN not configured.")
        return False
        
    url = f"https://graph.facebook.com/v19.0/{FB_PAGE_ID}/photos"
    try:
        with open(image_path, "rb") as img:
            files = {"source": img}
            data = {
                "caption": caption,
                "access_token": FB_PAGE_TOKEN
            }
            res = requests.post(url, data=data, files=files, timeout=40)
            res.raise_for_status()
            res_data = res.json()
            print(f"[Facebook] Successfully posted! Post ID: {res_data.get('id')}")
            return True
    except Exception as e:
        print(f"[Facebook] Post failed: {e}")
        if 'res' in locals():
            print(f"Details: {res.text}")
        return False

def post_to_instagram(public_image_url, caption):
    """
    Publishes an image post to Instagram Business Account via Meta Graph API.
    """
    if not IG_ACCOUNT_ID or not FB_PAGE_TOKEN:
        print("[Instagram] Skipped: INSTAGRAM_ACCOUNT_ID or FB_PAGE_ACCESS_TOKEN not configured.")
        return False
        
    if not public_image_url:
        print("[Instagram] Skipped: No public image URL available.")
        return False

    try:
        # Step 1: Create Media Container
        create_url = f"https://graph.facebook.com/v19.0/{IG_ACCOUNT_ID}/media"
        create_payload = {
            "image_url": public_image_url,
            "caption": caption,
            "access_token": FB_PAGE_TOKEN
        }
        create_res = requests.post(create_url, data=create_payload, timeout=30)
        create_res.raise_for_status()
        container_id = create_res.json().get("id")
        print(f"[Instagram] Media container created: {container_id}")

        # Wait 5 seconds for Instagram server to process image
        time.sleep(5)

        # Step 2: Publish Media Container
        publish_url = f"https://graph.facebook.com/v19.0/{IG_ACCOUNT_ID}/media_publish"
        publish_payload = {
            "creation_id": container_id,
            "access_token": FB_PAGE_TOKEN
        }
        pub_res = requests.post(publish_url, data=publish_payload, timeout=30)
        pub_res.raise_for_status()
        print(f"[Instagram] Successfully published! Post ID: {pub_res.json().get('id')}")
        return True
    except Exception as e:
        print(f"[Instagram] Post failed: {e}")
        return False

def post_to_linkedin(image_path, caption):
    """
    Publishes an image post to LinkedIn Profile or Organization Page.
    """
    if not LI_TOKEN or not LI_AUTHOR_URN:
        print("[LinkedIn] Skipped: LINKEDIN_ACCESS_TOKEN or LINKEDIN_AUTHOR_URN not configured.")
        return False

    headers = {
        "Authorization": f"Bearer {LI_TOKEN}",
        "X-Restli-Protocol-Version": "2.0.0",
        "Content-Type": "application/json"
    }

    try:
        # Step 1: Register upload
        register_url = "https://api.linkedin.com/v2/assets?action=registerUpload"
        register_payload = {
            "registerUploadRequest": {
                "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
                "owner": LI_AUTHOR_URN,
                "serviceRelationships": [{
                    "relationshipType": "OWNER",
                    "identifier": "urn:li:userGeneratedContent"
                }]
            }
        }
        reg_res = requests.post(register_url, headers=headers, json=register_payload, timeout=30)
        reg_res.raise_for_status()
        upload_data = reg_res.json()
        
        upload_url = upload_data["value"]["uploadMechanism"]["com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"]["uploadUrl"]
        asset_urn = upload_data["value"]["asset"]

        # Step 2: Upload image binary
        with open(image_path, "rb") as f:
            up_res = requests.post(upload_url, data=f, headers={"Authorization": f"Bearer {LI_TOKEN}"}, timeout=60)
            up_res.raise_for_status()

        # Step 3: Create UGC Post
        post_url = "https://api.linkedin.com/v2/ugcPosts"
        ugc_payload = {
            "author": LI_AUTHOR_URN,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": caption},
                    "shareMediaCategory": "IMAGE",
                    "media": [{
                        "status": "READY",
                        "description": {"text": "Graphic"},
                        "media": asset_urn,
                        "title": {"text": "Daily Insight"}
                    }]
                }
            },
            "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
        }

        post_res = requests.post(post_url, headers=headers, json=ugc_payload, timeout=30)
        post_res.raise_for_status()
        print(f"[LinkedIn] Successfully published! Post ID: {post_res.json().get('id')}")
        return True

    except Exception as e:
        print(f"[LinkedIn] Post failed: {e}")
        return False
