# StreamShift

## Overview

**StreamShift** is an intelligent video streaming solution that optimizes bandwidth usage by adjusting stream quality based on user activity. If you leave the screen or become distracted, **StreamShift** detects your absence and automatically reduces the video quality to save data. When you return to the screen, the video quality is restored to its optimal state. This adaptive bitrate streaming technology ensures that data is consumed efficiently while maintaining a seamless viewing experience.

## Features

- **Automatic Quality Adjustment**: The app detects user presence and adjusts video quality accordingly.
- **Bandwidth Optimization**: Reduces data consumption when the user is not actively watching, ensuring that bandwidth is used efficiently.
- **Seamless Streaming**: The quality change is smooth and does not disrupt your viewing experience when you return to the screen.
- **User Awareness**: Uses **OpenCV** to detect user attention and adjust the stream dynamically.
  
## Tech Stack

- **Frontend**: React, Node.js
- **Backend**: MongoDB, Express.js
- **Cloud**: [Cloud provider (e.g., AWS, GCP, Azure)] for hosting and streaming services.
- **User Detection**: OpenCV (for tracking user activity)
- **Network Limiting**: AHK scripts and network throttling tools for bandwidth control.
- **Adaptive Bitrate Streaming**: Custom implementation for smooth data consumption based on user presence.

## How It Works

1. **User Detection**: OpenCV tracks whether the user is actively watching the screen or not.
2. **Automatic Adjustment**: If the user is distracted or away, the stream quality is reduced to save bandwidth.
3. **Seamless Transition**: When the user returns to the screen, the stream quality is adjusted back to its highest level, ensuring a smooth experience.
4. **Data Saving**: The app throttles the network speed based on the user’s activity to optimize data usage without sacrificing the viewing experience.

## Contributing

We welcome contributions to **StreamShift**! If you'd like to contribute, please fork the repository, make your changes, and create a pull request. Be sure to follow the coding standards and best practices.

## Acknowledgments

- **OpenCV** for real-time user activity detection.
- **Cloudinary** for streaming and hosting services.
- **NetLimiter** for managing bandwidth.
