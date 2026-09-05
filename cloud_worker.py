import os
import requests

OUTPUT_DIR = "render_temp"
os.makedirs(OUTPUT_DIR, exist_ok=True)
out_file = os.path.join(OUTPUT_DIR, "queue_video.mp4")

# Reliable public MP4 clip
VIDEO_URL = "https://raw.githubusercontent.com/intel-iot-devkit/sample-videos/master/person-bicycle-car-detection.mp4"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

print("Downloading render payload...")
response = requests.get(VIDEO_URL, headers=headers, stream=True)
response.raise_for_status()

with open(out_file, "wb") as f:
    for chunk in response.iter_content(chunk_size=8192):
        f.write(chunk)

print("✓ Video file downloaded successfully.")
