import os
import yt_dlp

QUERY = "movie clip shorts"
OUTPUT_DIR = "render_temp"
ARCHIVE_FILE = "downloaded_archive.txt"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def is_downloaded(vid_id):
    if not os.path.exists(ARCHIVE_FILE):
        return False
    with open(ARCHIVE_FILE, "r") as f:
        return vid_id in f.read().splitlines()

def mark_downloaded(vid_id):
    with open(ARCHIVE_FILE, "a") as f:
        f.write(f"{vid_id}\n")

print("Searching YouTube...")
ydl_opts = {
    'extract_flat': 'in_playlist',
    'skip_download': True,
    'quiet': True,
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    res = ydl.extract_info(f"ytsearch10:{QUERY}", download=False)
    entries = res.get('entries', []) if res else []

target_id = next((e['id'] for e in entries if e and not is_downloaded(e['id'])), None)

if target_id:
    print(f"Target video found: {target_id}. Processing download...")
    out_file = os.path.join(OUTPUT_DIR, "queue_video.mp4")
    
    dl_opts = {
        'format': 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': out_file,
        'overwrites': True
    }
    
    with yt_dlp.YoutubeDL(dl_opts) as ydl:
        ydl.download([f"https://www.youtube.com/watch?v={target_id}"])
        
    if os.path.exists(out_file):
        mark_downloaded(target_id)
        print("✓ Video successfully downloaded.")
    else:
        raise FileNotFoundError("Output MP4 file was not generated.")
else:
    raise ValueError("No un-downloaded videos found matching search query.")
