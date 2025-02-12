const express = require('express');
const cloudinary = require('cloudinary').v2;
const multer = require('multer');
const path = require('path');
const mongoose = require('mongoose');
const Video = require('./models/videos');

require('dotenv').config();
require('./config/db');
cloudinary.config({
    cloud_name: process.env.CLOUDINARY_CLOUD_NAME,
    api_key: process.env.CLOUDINARY_API_KEY,
    api_secret: process.env.CLOUDINARY_API_SECRET
  });
  
const app = express();

const upload = multer({ dest: 'uploads/' });

app.use(express.static(path.join(__dirname, 'public')));
app.set('view engine', 'ejs');


app.get('/', (req, res) => {
    res.render('home');
  });

app.get('/add_video', (req, res) => {
  res.render('index');
});

app.post('/upload', upload.single('video'), (req, res) => {
    const filePath = req.file.path;
    const fileName = req.file.originalname;
  
    cloudinary.uploader.upload(
      filePath,
      {
        resource_type: 'video',
        public_id: 'user_video_' + Date.now(),  
        eager: [
          { streaming_profile: 'full_hd', format: 'm3u8' },
          { format: 'mp4', transformation: [{ quality: 'auto' }] },
        ],
        eager_async: true,
        eager_notification_url: "https://your-server.com/notification"
      },
      async (err, result) => {
        if (err) return res.status(500).json({ error: err.message });
  
        try {
          
          const pub_id = result.public_id;
  
          
          const video = new Video({
            PID: pub_id,       
            name: fileName,
            url: result.secure_url
          });
  
          
          await video.save();
  
          
          res.json({
            message: 'Video uploaded and data saved successfully!',
            videoUrl: result.secure_url,
            publicId: pub_id  
          });
        } catch (error) {
          res.status(500).json({ error: 'Error saving video metadata to MongoDB' });
        }
      }
    );
  });
  


app.get('/all_videos', async (req, res) => {
    try {
      const vids = await Video.find({});  
      res.render('all_video', { vids });  
    } catch (err) {
      console.error("Error fetching videos:", err);
      res.status(500).send("Error fetching videos");
    }
  });

app.get('/stream', (req, res) => {
  const networkSpeed = req.query.speed || 'high';
  let profile = 'full_hd';
  const pid = req.query.PID;
  if (networkSpeed === 'low') {
    profile = 'training_hd_h265';
  } else if (networkSpeed === 'medium') {
    profile = 'training_hd_vp9';
  }

  
  const cloudName = process.env.CLOUDINARY_CLOUD_NAME ;  //https://res.cloudinary.com/do6epdpbn/video/upload/v1725614181/user_video_1725614173678.mp4
  const publicId = pid;
  res.render('player', {cloudName, publicId });
});

app.post('/notification', (req, res) => {
  console.log('Transformation Complete:', req.body);
  res.status(200).send('Notification Received');
});

app.listen(3000, () => {
  console.log("Server running on port 3000");
});
