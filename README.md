# mp4converter (URL mode)

Backend Node.js (Express + FFmpeg) untuk menggabungkan poster (URL) dan audio (URL) jadi MP4.

## Deploy di Railway
1. Buat repo baru di GitHub dengan isi folder ini.
2. Hubungkan repo ke Railway.
3. Railway otomatis build pakai Dockerfile (FFmpeg sudah termasuk).

Endpoint: `POST /generate`
- JSON field: `posterUrl`, `audioUrl`

Output: MP4 (langsung download).
