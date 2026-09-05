import os
import requests

OUTPUT_DIR = "render_temp"
os.makedirs(OUTPUT_DIR, exist_ok=True)
out_file = os.path.join(OUTPUT_DIR, "queue_video.mp4")

# Reliable video source with custom headers to prevent 403 blocks
VIDEO_URL = "https://raw.githubusercontent.com/intel-iot-devkit/sample-videos/master/person-bicycle-car-detection.mp4"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

print("Downloading payload...")
res = requests.get(VIDEO_URL, headers=headers, stream=True)
res.raise_for_status()

with open(out_file, "wb") as f:
    for chunk in res.iter_content(chunk_size=8192):
        f.write(chunk)

print("✓ Video saved to render_temp/queue_video.mp4")
