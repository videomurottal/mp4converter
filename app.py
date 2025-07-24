from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
import subprocess
import os
import uuid

app = FastAPI()

@app.post("/upload")
async def convert_webm_to_mp4(file: UploadFile = File(...)):
    input_filename = f"/tmp/{uuid.uuid4()}.webm"
    output_filename = f"/tmp/{uuid.uuid4()}.mp4"

    with open(input_filename, "wb") as f:
        f.write(await file.read())

    command = [
        "ffmpeg",
        "-i", input_filename,
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "23",
        "-c:a", "aac",
        "-b:a", "128k",
        output_filename
    ]

    result = subprocess.run(command, capture_output=True)
    if result.returncode != 0:
        return {"error": "Conversion failed", "detail": result.stderr.decode()}

    def iterfile():
        with open(output_filename, mode="rb") as f:
            yield from f

    return StreamingResponse(iterfile(), media_type="video/mp4")
