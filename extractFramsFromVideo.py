import os
import cv2
import yt_dlp

# تنزيل الفيديو باستخدام yt-dlp
def download_video(youtube_url, download_path="video.mp4"):
    ydl_opts = {
        'outtmpl': download_path,
        'format': 'mp4',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])
    return download_path

# استخراج 100 فريم من الفيديو
def extract_frames(video_path, output_folder, frame_count=100):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    video_capture = cv2.VideoCapture(video_path)
    total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
    interval = total_frames // frame_count

    frame_idx = 0
    extracted_count = 0

    while True:
        ret, frame = video_capture.read()
        if not ret or extracted_count >= frame_count:
            break

        if frame_idx % interval == 0:
            frame_filename = os.path.join(output_folder, f"frame_{extracted_count + 1}.jpg")
            cv2.imwrite(frame_filename, frame)
            extracted_count += 1

        frame_idx += 1

    video_capture.release()

# الرابط إلى فيديو يوتيوب
youtube_url = "https://www.youtube.com/watch?v=snX5YyflrGw&ab_channel=MrBeast"

# مسار حفظ الفيديو
downloaded_video = download_video(youtube_url)

# استخراج 100 فريم وحفظها في المجلد "frames"
extract_frames(downloaded_video, output_folder="frames")
