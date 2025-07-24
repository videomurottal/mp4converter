from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import uuid
import os

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    temp_input = f"temp_{uuid.uuid4()}.webm"
    temp_output = temp_input.replace(".webm", ".mp4")

    with open(temp_input, "wb") as f:
        f.write(await file.read())

    try:
        subprocess.run(["ffmpeg", "-i", temp_input, "-c:v", "libx264", "-c:a", "aac", "-strict", "experimental", temp_output], check=True)
    except subprocess.CalledProcessError:
        return {"error": "Conversion failed"}
    finally:
        os.remove(temp_input)

    return FileResponse(temp_output, media_type="video/mp4", filename=temp_output)
