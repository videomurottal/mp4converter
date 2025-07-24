import express from 'express';
import cors from 'cors';
import fetch from 'node-fetch';
import { exec } from 'child_process';
import fs from 'fs';
import path from 'path';

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

app.post('/generate', async (req, res) => {
  try {
    const { posterUrl, audioUrl } = req.body;
    if (!posterUrl || !audioUrl) throw new Error('posterUrl dan audioUrl wajib dikirim');

    const posterPath = `downloads/poster.png`;
    const audioPath = `downloads/audio.mp3`;
    const outputPath = `downloads/output.mp4`;
    fs.mkdirSync('downloads', { recursive: true });

    // Download poster
    const posterRes = await fetch(posterUrl);
    if (!posterRes.ok) throw new Error('Gagal unduh poster');
    const posterBuffer = await posterRes.arrayBuffer();
    fs.writeFileSync(posterPath, Buffer.from(posterBuffer));

    // Download audio
    const audioRes = await fetch(audioUrl);
    if (!audioRes.ok) throw new Error('Gagal unduh audio');
    const audioBuffer = await audioRes.arrayBuffer();
    fs.writeFileSync(audioPath, Buffer.from(audioBuffer));

    // Jalankan FFmpeg
    await new Promise((resolve, reject) => {
      exec(
        `ffmpeg -y -loop 1 -i ${posterPath} -i ${audioPath} -c:v libx264 -tune stillimage -c:a aac -b:a 192k -shortest -pix_fmt yuv420p ${outputPath}`,
        (err) => (err ? reject(err) : resolve())
      );
    });

    res.download(outputPath, 'poster-video.mp4', () => {
      fs.unlinkSync(posterPath);
      fs.unlinkSync(audioPath);
      fs.unlinkSync(outputPath);
    });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Proses gagal', details: err.message });
  }
});

app.listen(PORT, () => console.log(`Server mp4converter (URL mode) jalan di port ${PORT}`));
