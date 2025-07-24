from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import subprocess

app = FastAPI()

@app.get("/")
def home():
    return {"message": "FastAPI WebM to MP4 converter is running"}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    input_path = "input.webm"
    output_path = "output.mp4"

    with open(input_path, "wb") as f:
        f.write(await file.read())

    # Jalankan ffmpeg
    subprocess.run(["ffmpeg", "-y", "-i", input_path, "-c:v", "libx264", output_path])

    return FileResponse(output_path, media_type="video/mp4", filename="converted.mp4")
