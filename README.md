# Subtitle API

A lightweight API to convert subtitle files (.srt or Whisper JSON) into .ass format with support for RTL, karaoke styling, and preview.

## Features

- Convert `.srt` or Whisper `.json` to `.ass`
- RTL support with directional markers
- Karaoke mode (`\k`) if word timings are present
- Word-by-word subtitle splitting
- VTT generation for browser preview
- HTML preview endpoint

## Run locally

```
docker-compose up --build
```

Then open: http://localhost:8080/docs