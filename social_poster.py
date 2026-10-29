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

def post_carousel_to_facebook(image_paths, caption):
    """
    Publishes a multi-image carousel post to Facebook Page.
    1. Uploads each photo with published=false.
    2. Publishes a feed post with attached_media referencing all uploaded photos.
    """
    token = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN", FB_PAGE_TOKEN)
    page_id = os.getenv("FACEBOOK_PAGE_ID", FB_PAGE_ID)

    if not page_id or not token:
        print("[Facebook Carousel] Skipped: Missing credentials.")
        return False

    try:
        import json
        photo_ids = []
        upload_url = f"https://graph.facebook.com/v19.0/{page_id}/photos"

        for idx, img_path in enumerate(image_paths):
            print(f"[Facebook Carousel] Uploading slide {idx + 1}/{len(image_paths)}: {img_path}")
            with open(img_path, "rb") as f:
                res = requests.post(
                    upload_url,
                    data={"published": "false", "access_token": token},
                    files={"source": f},
                    timeout=30
                )
                res.raise_for_status()
                pid = res.json().get("id")
                photo_ids.append(pid)

        # Publish the feed post with attached media
        feed_url = f"https://graph.facebook.com/v19.0/{page_id}/feed"
        attached_media = [{"media_fbid": pid} for pid in photo_ids]
        payload = {
            "message": caption,
            "attached_media": json.dumps(attached_media),
            "access_token": token
        }
        feed_res = requests.post(feed_url, data=payload, timeout=30)
        feed_res.raise_for_status()
        post_id = feed_res.json().get("id")
        print(f"[Facebook Carousel] Successfully published carousel! Post ID: {post_id}")
        return True
    except Exception as e:
        print(f"[Facebook Carousel] Post failed: {e}")
        return False

def post_carousel_to_instagram(image_paths, caption):
    """
    Publishes a multi-image carousel post to Instagram Business (@tauhidadslab).
    1. Uploads each slide publicly and creates carousel item containers.
    2. Creates parent CAROUSEL container.
    3. Publishes the carousel container.
    """
    token = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN", FB_PAGE_TOKEN)
    ig_id = os.getenv("INSTAGRAM_ACCOUNT_ID", IG_ACCOUNT_ID)

    if not ig_id or not token:
        print("[Instagram Carousel] Skipped: Missing credentials.")
        return False

    try:
        import json
        item_container_ids = []
        for idx, img_path in enumerate(image_paths):
            pub_url = upload_image_public(img_path)
            if not pub_url:
                print(f"[Instagram Carousel] Could not upload slide {idx + 1}")
                continue
            create_url = f"https://graph.facebook.com/v19.0/{ig_id}/media"
            c_res = requests.post(
                create_url,
                data={"image_url": pub_url, "is_carousel_item": "true", "access_token": token},
                timeout=30
            )
            c_res.raise_for_status()
            item_id = c_res.json().get("id")
            item_container_ids.append(item_id)
            time.sleep(2)

        if not item_container_ids:
            print("[Instagram Carousel] Failed: No slides uploaded.")
            return False

        # Create parent carousel container
        parent_url = f"https://graph.facebook.com/v19.0/{ig_id}/media"
        parent_res = requests.post(
            parent_url,
            data={
                "media_type": "CAROUSEL",
                "children": json.dumps(item_container_ids),
                "caption": caption,
                "access_token": token
            },
            timeout=30
        )
        parent_res.raise_for_status()
        parent_id = parent_res.json().get("id")

        print("[Instagram Carousel] Waiting 12 seconds for container rendering...")
        time.sleep(12)

        # Publish
        pub_url = f"https://graph.facebook.com/v19.0/{ig_id}/media_publish"
        pub_res = requests.post(
            pub_url,
            data={"creation_id": parent_id, "access_token": token},
            timeout=30
        )
        pub_res.raise_for_status()
        post_id = pub_res.json().get("id")
        print(f"[Instagram Carousel] Successfully published to @tauhidadslab! Post ID: {post_id}")
        return True
    except Exception as e:
        print(f"[Instagram Carousel] Post failed: {e}")
        return False

def post_carousel_to_linkedin(image_paths, caption):
    """
    Publishes a multi-image swipeable carousel post to LinkedIn.
    1. Registers each slide image via v2/assets using 'urn:li:digitalmediaRecipe:feedshare-image'.
    2. Uploads the binary image data via PUT to the pre-signed uploadUrl.
    3. Publishes via v2/ugcPosts with shareMediaCategory: IMAGE and media list.
    LinkedIn natively displays this as an interactive multi-image carousel on the feed.
    """
    token = os.getenv("LINKEDIN_ACCESS_TOKEN", LI_TOKEN)
    urn = os.getenv("LINKEDIN_AUTHOR_URN", LI_AUTHOR_URN)

    if not token or not urn:
        print("[LinkedIn Carousel] Skipped: Missing credentials.")
        return False

    headers = {
        "Authorization": f"Bearer {token}",
        "X-Restli-Protocol-Version": "2.0.0",
        "Content-Type": "application/json"
    }

    try:
        media_assets = []
        register_url = "https://api.linkedin.com/v2/assets?action=registerUpload"

        # Up to 9 images supported on LinkedIn multi-image post
        for idx, img_path in enumerate(image_paths[:9]):
            print(f"[LinkedIn Carousel] Registering slide {idx + 1}/{len(image_paths)}: {img_path}")
            reg_payload = {
                "registerUploadRequest": {
                    "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
                    "owner": urn,
                    "serviceRelationships": [{
                        "relationshipType": "OWNER",
                        "identifier": "urn:li:userGeneratedContent"
                    }]
                }
            }
            reg_res = requests.post(register_url, headers=headers, json=reg_payload, timeout=30)
            if reg_res.status_code != 200:
                print(f"[LinkedIn Carousel] Error registering slide {idx + 1}: {reg_res.text}")
                continue

            upload_data = reg_res.json()
            upload_url = upload_data["value"]["uploadMechanism"]["com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"]["uploadUrl"]
            asset_urn = upload_data["value"]["asset"]

            # Step 2: Upload binary image using PUT
            with open(img_path, "rb") as f:
                file_bytes = f.read()
                put_headers = {
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "image/png"
                }
                up_res = requests.put(upload_url, data=file_bytes, headers=put_headers, timeout=60)
                if up_res.status_code not in (200, 201):
                    # Fallback to POST
                    up_res = requests.post(upload_url, data=file_bytes, headers=put_headers, timeout=60)

            media_assets.append({
                "status": "READY",
                "description": {"text": f"Slide {idx + 1}"},
                "media": asset_urn,
                "title": {"text": f"Slide {idx + 1}"}
            })

        if not media_assets:
            print("[LinkedIn Carousel] Failed: No slides were successfully uploaded.")
            return False

        print(f"[LinkedIn Carousel] Publishing multi-image carousel ({len(media_assets)} slides)...")
        post_url = "https://api.linkedin.com/v2/ugcPosts"
        ugc_payload = {
            "author": urn,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": caption},
                    "shareMediaCategory": "IMAGE",
                    "media": media_assets
                }
            },
            "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
        }

        post_res = requests.post(post_url, headers=headers, json=ugc_payload, timeout=30)
        post_res.raise_for_status()
        post_id = post_res.json().get("id")
        print(f"[LinkedIn Carousel] Successfully published multi-image carousel! Post ID: {post_id}")
        return True

    except Exception as e:
        print(f"[LinkedIn Carousel] Post failed: {e}")
        if 'post_res' in locals():
            print(f"Details: {post_res.text}")
        return False

def post_document_to_linkedin(pdf_path, caption, title="Shopify & GA4 Tracking Blueprint", image_paths=None):
    """
    Publishes carousel to LinkedIn. If image_paths is provided, publishes as a
    multi-image carousel (guaranteed 100% compatibility with LinkedIn's public API permissions).
    """
    if image_paths and len(image_paths) > 0:
        return post_carousel_to_linkedin(image_paths, caption)
    token = os.getenv("LINKEDIN_ACCESS_TOKEN", LI_TOKEN)
    urn = os.getenv("LINKEDIN_AUTHOR_URN", LI_AUTHOR_URN)

    if not token or not urn:
        print("[LinkedIn Document] Skipped: Missing credentials.")
        return False

    headers = {
        "Authorization": f"Bearer {token}",
        "X-Restli-Protocol-Version": "2.0.0",
        "Content-Type": "application/json"
    }

    try:
        # Step 1: Register document upload
        register_url = "https://api.linkedin.com/v2/assets?action=registerUpload"
        register_payload = {
            "registerUploadRequest": {
                "recipes": ["urn:li:digitalmediaRecipe:feedshare-document"],
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

        # Step 2: Upload PDF binary via PUT
        with open(pdf_path, "rb") as f:
            up_res = requests.put(
                upload_url,
                data=f,
                headers={"Authorization": f"Bearer {token}", "Content-Type": "application/pdf"},
                timeout=60
            )
            up_res.raise_for_status()

        # Step 3: Create UGC Post with shareMediaCategory DOCUMENT
        post_url = "https://api.linkedin.com/v2/ugcPosts"
        ugc_payload = {
            "author": urn,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": caption},
                    "shareMediaCategory": "DOCUMENT",
                    "media": [{
                        "status": "READY",
                        "description": {"text": title},
                        "media": asset_urn,
                        "title": {"text": title}
                    }]
                }
            },
            "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
        }

        post_res = requests.post(post_url, headers=headers, json=ugc_payload, timeout=30)
        post_res.raise_for_status()
        post_id = post_res.json().get("id")
        print(f"[LinkedIn Document Carousel] Successfully published! Post ID: {post_id}")
        return True
    except Exception as e:
        print(f"[LinkedIn Document Carousel] Post failed: {e}")
        return False
