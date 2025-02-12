const mongoose = require('mongoose');

// Define Video Schema
const videoSchema = new mongoose.Schema({
  PID : { type:String , required :true},
  name: { type: String, required: true },
  url: { type: String, required: true },
  createdAt: { type: Date, default: Date.now }
});

// Create and export the Video model
const Video = mongoose.model('Video', videoSchema);
module.exports = Video;
