This guide explains how to work with the Subtitle API using an LLM Agent to process Hebrew subtitle files intelligently — from transcription to preview to export.

---

## 🎯 Goal

To enable the agent to:

1. Receive a video file or link
2. Transcribe it using Whisper API
3. Process the subtitle file with advanced settings (RTL, styling, karaoke, word-by-word)
4. Preview the results on the video
5. Download the final `.ass` file for further embedding or delivery

---

## 🧩 Step-by-Step Workflow

### 1. 🔊 Transcribe Video with Whisper API

Use OpenAI Whisper API (or whisper.cpp, if local) with:

```json
{
  "response_format": "verbose_json",
  "word_timestamps": true,
  "language": "he"
}
```

This provides a JSON with per-word timing necessary for karaoke or word-by-word rendering.

---

### 2. 📤 Call `/api/convert`

Make a `POST` request to the Subtitle API:

- **file**: The `.srt` or `.json` file (from Whisper)
- **config**: A stringified JSON with subtitle processing options
- **video_url** *(optional)*: A URL to the original video for preview
- **video_file** *(optional)*: A video uploaded directly to the API

The response will include:

```json
{
  "ass_url": "/download/{id}.ass",
  "preview_url": "/preview/{id}",
  "video_url": "https://..."
}
```

---

## ⚙️ JSON Config Options

These are the full available options for `config`:

```json
{
  "rtl": true,
  "karaoke": false,
  "word_by_word": false,
  "delay_ms": -300,
  "max_line_length": 42,
  "replace_terms": {
    "(מוזיקה)": "",
    "[צחוק]": ""
  },
  "style": {
    "font": "David",
    "font_size": 24,
    "primary_color": "white",
    "outline_color": "black",
    "bold": true,
    "alignment": "bottom"
  }
}
```

### 🔍 Explanation

| Option | Description |
|--------|-------------|
| `rtl` | Apply RTL direction to all lines (adds Unicode markers) |
| `karaoke` | Use `\k` tags to highlight words with per-word timing |
| `word_by_word` | Split each word into a separate subtitle line |
| `delay_ms` | Shift subtitle timing (positive or negative) |
| `max_line_length` | Automatically split long lines (not yet implemented) |
| `replace_terms` | Dictionary of search → replace strings |
| `style` | Visual style for `.ass` output (font, size, color, etc.) |

Note: Only one of `karaoke` or `word_by_word` should be `true`.

---

### 3. 👀 Preview the Result

Use the `preview_url` in a browser or WebView. This will display:

- The uploaded/provided video
- The converted subtitle file (as `.vtt` preview)
- Useful for checking synchronization and formatting

---

### 4. 📥 Download Final File

Use `ass_url` to download the final `.ass` subtitle file, suitable for:

- Embedding into video with FFmpeg
- Sharing with clients or users
- Uploading to subtitle platforms

---

## 🧠 Agent Logic Summary

```plaintext
IF input is video:
    → transcribe with Whisper (verbose_json, word_timestamps=true)
    → send to /api/convert with proper config
    → preview the output
    → optionally trigger FFmpeg render using .ass
```

---

Need to support CLI tools or automatic rendering? Combine with a renderer service that accepts `.ass` and `.mp4`.
