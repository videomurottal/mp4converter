from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import shutil
import os
import uuid

app = FastAPI()

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    webm_path = f"temp_{uuid.uuid4()}.webm"
    mp4_path = webm_path.replace(".webm", ".mp4")

    with open(webm_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Convert to MP4 using ffmpeg
    os.system(f"ffmpeg -i {webm_path} -c:v libx264 -preset fast -crf 22 -c:a aac -b:a 128k {mp4_path}")

    os.remove(webm_path)
    return FileResponse(mp4_path, media_type="video/mp4", filename=os.path.basename(mp4_path))
