# LLM Agent Integration

This API supports automated workflows to process subtitle files for Hebrew videos.

## Workflow

1. Transcribe using Whisper API with:
   - `response_format: "verbose_json"`
   - `word_timestamps: true`

2. POST to `/api/convert` with:
   - `file`: the .srt or .json file
   - `config`: JSON string of options
   - `video_url` or `video_file` for preview

3. Use returned `preview_url` to check results

4. Download final `.ass` file via `ass_url`