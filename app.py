from flask import Flask, request, send_file
import os, subprocess, uuid

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return '🚀 FFMPEG server running!'

@app.route('/convert', methods=['POST'])
def convert():
    file = request.files['video']
    if not file.filename.endswith('.webm'):
        return 'Invalid file type', 400

    input_path = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4()}.webm")
    output_path = input_path.replace('.webm', '.mp4')
    file.save(input_path)

    subprocess.run([
        'ffmpeg', '-y', '-i', input_path,
        '-c:v', 'libx264', '-c:a', 'aac', '-strict', 'experimental',
        output_path
    ])

    return send_file(output_path, as_attachment=True)
