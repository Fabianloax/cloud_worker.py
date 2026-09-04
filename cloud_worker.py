import os
import yt_dlp

QUERY = "movie clip shorts"
OUTPUT_DIR = "render_temp"
ARCHIVE_FILE = "downloaded_archive.txt"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def is_downloaded(vid_id):
    return os.path.exists(ARCHIVE_FILE) and vid_id in open(ARCHIVE_FILE).read().splitlines()

def mark_downloaded(vid_id):
    with open(ARCHIVE_FILE, "a") as f:
        f.write(f"{vid_id}\n")

# Search YouTube
ydl_opts = {'extract_flat': 'in_playlist', 'skip_download': True, 'quiet': True}
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    entries = ydl.extract_info(f"ytsearch10:{QUERY}", download=False).get('entries', [])

target_id = next((e['id'] for e in entries if e and not is_downloaded(e['id'])), None)

if target_id:
    out_file = os.path.join(OUTPUT_DIR, "queue_video.mp4")
    filter_arg = "drawtext=text='SUBSCRIBE FOR MORE':fontcolor=yellow:fontsize=32:box=1:boxcolor=black@0.75:boxborderw=12:x=(w-text_w)/2:y=h-200"
    
    dl_opts = {
        'format': 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': out_file,
        'postprocessor_args': {'ffmpeg': ['-vf', filter_arg, '-c:v', 'libx264', '-crf', '18', '-preset', 'fast']}
    }
    
    with yt_dlp.YoutubeDL(dl_opts) as ydl:
        ydl.download([f"https://www.youtube.com/watch?v={target_id}"])
        
    if os.path.exists(out_file):
        mark_downloaded(target_id)
        print("✓ Video rendered and ready for upload artifact.")
