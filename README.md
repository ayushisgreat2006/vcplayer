# STARK MUSIC — Next-Gen Telegram Music Player

A production-ready Telegram Voice Chat music bot using:
- Pyrogram (bot + user client)
- PyTgCalls for VC streaming
- yt-dlp & ffmpeg for media
- MongoDB (motor) for persistence

## Features
- /play <query|url>
- /pause, /resume, /skip, /stop
- /queue, /current
- Admin system & global ban
- Auto-join VC and auto-leave when queue empty
- Download, convert, stream from YouTube & direct URLs
- Inline-friendly scaffold

## Requirements
- Python 3.10+
- ffmpeg (system)
- MongoDB (URI)
- Telegram bot token, API_ID, API_HASH, owner id, assistant string session, assistant id

## Environment Vars
Set these in your environment (Railway/Render/etc):
