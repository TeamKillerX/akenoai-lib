# All credits to @xpushz on Telegram
# You can use this for a WhatsApp Userbot or other platforms
# If you're building a Telegram Story Downloader website like my Story TG DL API

import base64
import time

import requests

API_BASE_URL = "https://randydev-ryu-js.hf.space/api/v1"
API_KEY = "akeno_xxxxxxx"

def story_response_call(response):
    if response["status"] == "completed":
        video_path = "downloaded_story.mp4"
        with open(video_path, "wb") as f:
            f.write(base64.b64decode(response["story_bytes"]))
        return video_path
    return None

def story_task_now_call(story_url):
    url = f"{API_BASE_URL}/user/story/task"
    headers = {"x-api-key": API_KEY}
    params = {"story_url": story_url}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json().get("job_id")
    return None

def check_job_status(job_id):
    url = f"{API_BASE_URL}/user/story/task/{job_id}"
    headers = {"x-api-key": API_KEY}

    while True:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data["status"] in ["completed", "failed"]:
                return data
        time.sleep(5)

job_id = story_task_now_call("https://t.me/username/s/1")
if job_id:
    print(f"Job started with ID: {job_id}")
    response = check_job_status(job_id)
    if response["status"] == "completed":
        saved_file = story_response_call(response)
        print(f"Story saved at: {saved_file}")
    else:
        print("Story download failed or still processing.")
else:
    print("Failed to start story download task.")
