from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse
import uuid, os, subprocess

app = FastAPI()

@app.post("/upload")
async def upload(file: UploadFile):
    temp_webm = f"/tmp/{uuid.uuid4()}.webm"
    temp_mp4 = temp_webm.replace(".webm", ".mp4")

    with open(temp_webm, "wb") as f:
        f.write(await file.read())

    subprocess.run([
        "ffmpeg", "-i", temp_webm,
        "-c:v", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p",
        temp_mp4
    ])

    return {"url": f"/download/{os.path.basename(temp_mp4)}"}

@app.get("/download/{filename}")
async def download(filename: str):
    return FileResponse(f"/tmp/{filename}", media_type="video/mp4", filename=filename)
