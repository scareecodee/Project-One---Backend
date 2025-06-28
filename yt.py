# main.py
import os
import yt_dlp
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI()

# CORS setup for Android app communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DownloadRequest(BaseModel):
    video_url: str
    quality: str

@app.post("/video/download")
def download_and_merge_video(req: DownloadRequest):
    try:
        os.makedirs("temp", exist_ok=True)
        quality_num = req.quality.replace("p", "")
        ydl_opts = {
    'format': f'bestvideo[height<={quality_num}]+bestaudio/best[height<={quality_num}]',
    'outtmpl': f'temp/%(title)s_{quality_num}p.%(ext)s',
    'merge_output_format': 'mp4',
    'quiet': True,
}

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(req.video_url, download=True)
            filename = ydl.prepare_filename(info).rsplit(".", 1)[0] + ".mp4"

        return {"success": True, "filename": os.path.basename(filename)}

    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/video/download-file")
def get_downloaded_file(filename: str, background_tasks: BackgroundTasks):
    filepath = f"temp/{filename}"
    if os.path.exists(filepath):
        background_tasks.add_task(os.remove, filepath)
        return FileResponse(filepath, media_type="video/mp4", filename=filename)
    return {"success": False, "error": "File not found"}



# main.py
import yt_dlp
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List


# CORS config (allow all origins for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



class VideoInfoRequest(BaseModel):
    video_url: str

class VideoInfoResponse(BaseModel):
    success: bool
    qualities: List[str] = []
    title: str = ""
    error: str = None


@app.post("/video/get-qualities", response_model=VideoInfoResponse)
def get_available_qualities(req: VideoInfoRequest):
    try:
        # Fetch video metadata
        ydl_opts = {
            'quiet': True,
            'skip_download': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(req.video_url, download=False)

        # Extract video qualities
        qualities_set = set()
        for fmt in info.get("formats", []):
            height = fmt.get("height")
            if height and fmt.get("vcodec") != "none":
                qualities_set.add(f"{height}p")

        qualities_list = sorted(qualities_set, key=lambda x: int(x.replace("p", "")))

        return VideoInfoResponse(
            success=True,
            qualities=qualities_list,
            title=info.get("title", "Unknown Title")
        )

    except Exception as e:
        return VideoInfoResponse(success=False, error=str(e))





class AudioRequest(BaseModel):
    video_url: str

@app.post("/audio/download")
def download_best_audio(req: AudioRequest):
    try:
        os.makedirs("temp", exist_ok=True)
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'temp/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(req.video_url, download=True)
            filename = ydl.prepare_filename(info).rsplit('.', 1)[0] + ".mp3"

        return {"success": True, "filename": os.path.basename(filename)}

    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/audio/file")
def get_audio_file(filename: str, background_tasks: BackgroundTasks):
    path = f"temp/{filename}"
    if os.path.exists(path):
        background_tasks.add_task(os.remove, path)
        return FileResponse(path, media_type="audio/mpeg", filename=filename)
    return {"success": False, "error": "File not found"}







from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import smtplib
from email.mime.text import MIMEText
import random



# ⚡️ Model for request
class EmailRequest(BaseModel):
    email: str

@app.post("/send_otp/")
def send_otp(request: EmailRequest):
    receiver_email = request.email
    otp = random.randint(100000, 999999)

    # ✅ Email details
    sender_email = "godofgenjutsu890@gmail.com"
    app_password = "zxhf dhds yvgm vnou"
    subject = "Your Verification OTP - Zebyte App"
    body = f'''Thank you for using Zebyte!
To complete your verification, please use the one-time password (OTP) below:
OTP:{otp}
If you did not request this code, you can safely ignore this email.

Thank you for choosing Zebyte!

Best regards,
The Zebyte Team'''

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    try:
        # ✅ Connect to Gmail SMTP
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, app_password)
            server.send_message(msg)

        return {"status": "success", "otp": otp}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending email: {str(e)}")


