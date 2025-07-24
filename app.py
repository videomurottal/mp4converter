@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    # Simpan file sementara
    temp_input = "temp_input.webm"
    temp_output = "output.mp4"
    with open(temp_input, "wb") as f:
        f.write(await file.read())

    # Konversi dengan ffmpeg
    cmd = f"ffmpeg -y -i {temp_input} -c:v libx264 -c:a aac -strict experimental {temp_output}"
    subprocess.run(cmd.split(), check=True)

    return FileResponse(temp_output, media_type="video/mp4", filename="converted.mp4")
