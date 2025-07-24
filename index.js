import express from 'express';
import cors from 'cors';
import multer from 'multer';
import fetch from 'node-fetch';
import { exec } from 'child_process';
import fs from 'fs';
import path from 'path';

const app = express();
const upload = multer({ dest: 'uploads/' });
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

app.post('/generate', upload.single('poster'), async (req, res) => {
  try {
    const { audioUrl } = req.body;
    const posterPath = req.file.path;
    const audioPath = `uploads/audio.mp3`;
    const outputPath = `uploads/output.mp4`;

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

app.listen(PORT, () => console.log(`Server mp4converter jalan di port ${PORT}`));
