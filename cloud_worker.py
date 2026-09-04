import os
import requests

OUTPUT_DIR = "render_temp"
os.makedirs(OUTPUT_DIR, exist_ok=True)
out_file = os.path.join(OUTPUT_DIR, "queue_video.mp4")

# Direct royalty-free sample clip URL
VIDEO_URL = "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4"

print("Downloading render payload...")
response = requests.get(VIDEO_URL, stream=True)
response.raise_for_status()

with open(out_file, "wb") as f:
    for chunk in response.iter_content(chunk_size=8192):
        f.write(chunk)

print("✓ Video file ready for artifact packaging.")
