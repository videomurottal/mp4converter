from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
import subprocess, uuid, os
import requests

app = FastAPI()

@app.get("/")
def home():
    return {"status": "ready", "usage": "/convert?video=URL&audio=URL"}

@app.get("/convert")
def convert(video: str, audio: str):
    os.makedirs("temp", exist_ok=True)
    id = str(uuid.uuid4())
    video_path = f"temp/{id}.webm"
    audio_path = f"temp/{id}.mp3"
    output_path = f"temp/{id}.mp4"

    with open(video_path, "wb") as f:
        f.write(requests.get(video).content)
    with open(audio_path, "wb") as f:
        f.write(requests.get(audio).content)

    subprocess.run([
        "ffmpeg", "-i", video_path, "-i", audio_path,
        "-c:v", "copy", "-c:a", "aac", "-strict", "experimental", output_path
    ], check=True)

    return FileResponse(output_path, media_type="video/mp4", filename="result.mp4")
