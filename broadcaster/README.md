# USALB Radio 24 Broadcaster

This is the Windows live-broadcast app for **USALB Radio 24**.

It is designed for the setup we are building:

**Windows PC → USALB Radio 24 AzuraCast/Icecast → Internet listeners**

## Features

- Simple Windows desktop interface
- Start/Stop live broadcast
- Select an audio file
- Optional microphone input
- MP3 encoding at 128 kbps
- Direct Icecast connection
- Live connection log
- No paid streaming service

## Requirements

- Windows 10/11
- Python 3.11+
- FFmpeg installed and available as `ffmpeg.exe` in PATH

## First run

1. Install Python.
2. Install FFmpeg.
3. Run `start.bat`.
4. Enter the streamer password created in AzuraCast.
5. Choose an audio file or microphone.
6. Press **START LIVE**.

## Connection defaults

These defaults match the AzuraCast station information supplied during setup:

- Server: `79.106.124.110`
- Port: `8005`
- Mount: `/`
- Username: `usalb`

The password is intentionally **not stored in GitHub**.

## Security

Never commit the real AzuraCast streamer password to this repository.
