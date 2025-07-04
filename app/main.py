from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from uuid import uuid4
import shutil
import json
from app.subtitle_utils import process_subtitles
from pathlib import Path

app = FastAPI(
    title="Subtitle API",
    description="Convert SRT or Whisper JSON to ASS (with RTL, Karaoke, and Preview support)",
    version="1.0.0"
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

TEMP_DIR = Path("static")
SUB_DIR = TEMP_DIR / "subtitles"
VID_DIR = TEMP_DIR / "videos"

@ app.post("/api/convert")
async def convert_subtitles(
    file: UploadFile = File(..., description="SRT or Whisper JSON file"),
    config: str = Form(..., description="JSON string with processing options"),
    video_url: str = Form(None, description="Optional URL to video for preview"),
    video_file: UploadFile = File(None, description="Optional uploaded video file for preview")
):
    uid = str(uuid4())
    srt_path = SUB_DIR / f"{uid}{Path(file.filename).suffix}"
    ass_path = SUB_DIR / f"{uid}.ass"
    vtt_path = SUB_DIR / f"{uid}.vtt"
    video_path = None

    with open(srt_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    config_data = json.loads(config)
    process_subtitles(srt_path, ass_path, vtt_path, config_data)

    if video_file:
        video_path = VID_DIR / f"{uid}_{video_file.filename}"
        with open(video_path, "wb") as f:
            shutil.copyfileobj(video_file.file, f)
    elif video_url:
        video_path = video_url

    return {
        "ass_url": f"/download/{uid}.ass",
        "preview_url": f"/preview/{uid}",
        "video_url": str(video_path) if video_path else None
    }

@ app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = SUB_DIR / filename
    return FileResponse(path=file_path, filename=filename)

@ app.get("/preview/{uid}", response_class=HTMLResponse)
async def preview(uid: str):
    video_files = list(VID_DIR.glob(f"{uid}_*"))
    video_path = f"/static/videos/{video_files[0].name}" if video_files else ""
    return HTMLResponse(Path("templates/preview.html").read_text().replace("{{VIDEO_PATH}}", video_path).replace("{{SUB_PATH}}", f"/download/{uid}.vtt"))

@app.get("/health")
def health_check():
    return {"status": "ok"}
