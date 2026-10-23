import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

# Meta credentials
FB_PAGE_ID = os.getenv("FACEBOOK_PAGE_ID")
FB_PAGE_TOKEN = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN")
IG_ACCOUNT_ID = os.getenv("INSTAGRAM_ACCOUNT_ID", "17841435015705100")

# LinkedIn credentials
LI_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN")
LI_AUTHOR_URN = os.getenv("LINKEDIN_AUTHOR_URN")

# Image hosting for Instagram (ImgBB or free direct host)
IMGBB_API_KEY = os.getenv("IMGBB_API_KEY")

def upload_image_public(image_path):
    """
    Uploads the local graphic to obtain a public HTTPS URL.
    Instagram Graph API strictly requires an HTTPS URL to fetch the image.
    Uses catbox.moe with ImgBB fallback.
    """
    # 1. Try Catbox (fast, free, zero setup)
    try:
        url = "https://catbox.moe/user/api.php"
        with open(image_path, "rb") as file:
            payload = {"reqtype": "fileupload"}
            files = {"fileToUpload": file}
            res = requests.post(url, data=payload, files=files, timeout=30)
            if res.status_code == 200 and res.text.startswith("http"):
                public_url = res.text.strip()
                print(f"[Public Upload] Image uploaded via Catbox: {public_url}")
                return public_url
    except Exception as e:
        print(f"[Public Upload] Catbox attempt failed: {e}")

    # 2. Try ImgBB if key is available
    if IMGBB_API_KEY:
        try:
            url = "https://api.imgbb.com/1/upload"
            with open(image_path, "rb") as file:
                payload = {"key": IMGBB_API_KEY}
                files = {"image": file}
                res = requests.post(url, data=payload, files=files, timeout=30)
                if res.status_code == 200:
                    public_url = res.json()["data"]["url"]
                    print(f"[Public Upload] Image uploaded via ImgBB: {public_url}")
                    return public_url
        except Exception as e:
            print(f"[Public Upload] ImgBB attempt failed: {e}")

    print("[Public Upload] Could not generate public HTTPS image URL for Instagram.")
    return None

def post_to_facebook(image_path, caption):
    """
    Publishes an image post to Facebook Page.
    """
    token = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN", FB_PAGE_TOKEN)
    page_id = os.getenv("FACEBOOK_PAGE_ID", FB_PAGE_ID)

    if not page_id or not token:
        print("[Facebook] Skipped: FB_PAGE_ID or FB_PAGE_ACCESS_TOKEN not configured.")
        return False
        
    url = f"https://graph.facebook.com/v19.0/{page_id}/photos"
    try:
        with open(image_path, "rb") as img:
            files = {"source": img}
            data = {
                "caption": caption,
                "access_token": token
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

def post_to_instagram(image_path_or_url, caption):
    """
    Publishes an image post to Instagram Business Account (@tauhidadslab) via Meta Graph API.
    """
    token = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN", FB_PAGE_TOKEN)
    ig_id = os.getenv("INSTAGRAM_ACCOUNT_ID", IG_ACCOUNT_ID)

    if not ig_id or not token:
        print("[Instagram] Skipped: INSTAGRAM_ACCOUNT_ID or FB_PAGE_ACCESS_TOKEN not configured.")
        return False

    # Get public URL if given local file path
    if os.path.exists(image_path_or_url):
        public_url = upload_image_public(image_path_or_url)
    else:
        public_url = image_path_or_url

    if not public_url:
        print("[Instagram] Skipped: No public image URL available.")
        return False

    try:
        # Step 1: Create Media Container
        create_url = f"https://graph.facebook.com/v19.0/{ig_id}/media"
        create_payload = {
            "image_url": public_url,
            "caption": caption,
            "access_token": token
        }
        create_res = requests.post(create_url, data=create_payload, timeout=30)
        create_res.raise_for_status()
        container_id = create_res.json().get("id")
        print(f"[Instagram] Media container created: {container_id}")

        # Wait 8 seconds for Instagram server to process image
        time.sleep(8)

        # Step 2: Publish Media Container
        publish_url = f"https://graph.facebook.com/v19.0/{ig_id}/media_publish"
        publish_payload = {
            "creation_id": container_id,
            "access_token": token
        }
        pub_res = requests.post(publish_url, data=publish_payload, timeout=30)
        pub_res.raise_for_status()
        post_id = pub_res.json().get("id")
        print(f"[Instagram] Successfully published to @tauhidadslab! Post ID: {post_id}")
        return True
    except Exception as e:
        print(f"[Instagram] Post failed: {e}")
        if 'create_res' in locals():
            print(f"Create details: {create_res.text}")
        if 'pub_res' in locals():
            print(f"Publish details: {pub_res.text}")
        return False

def post_to_linkedin(image_path, caption):
    """
    Publishes an image post to LinkedIn Profile or Organization Page.
    """
    token = os.getenv("LINKEDIN_ACCESS_TOKEN", LI_TOKEN)
    urn = os.getenv("LINKEDIN_AUTHOR_URN", LI_AUTHOR_URN)

    if not token or not urn:
        print("[LinkedIn] Skipped: LINKEDIN_ACCESS_TOKEN or LINKEDIN_AUTHOR_URN not configured.")
        return False

    headers = {
        "Authorization": f"Bearer {token}",
        "X-Restli-Protocol-Version": "2.0.0",
        "Content-Type": "application/json"
    }

    try:
        # Step 1: Register upload
        register_url = "https://api.linkedin.com/v2/assets?action=registerUpload"
        register_payload = {
            "registerUploadRequest": {
                "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
                "owner": urn,
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
            up_res = requests.post(upload_url, data=f, headers={"Authorization": f"Bearer {token}"}, timeout=60)
            up_res.raise_for_status()

        # Step 3: Create UGC Post
        post_url = "https://api.linkedin.com/v2/ugcPosts"
        ugc_payload = {
            "author": urn,
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
