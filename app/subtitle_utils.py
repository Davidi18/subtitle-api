import pysubs2
import json
from datetime import timedelta

def process_subtitles(srt_path, ass_path, vtt_path, config):
    is_json = srt_path.suffix.lower() == ".json"

    if is_json:
        with open(srt_path, "r", encoding="utf-8") as f:
            whisper_data = json.load(f)
        subs = pysubs2.SSAFile()

        if config.get("word_by_word"):
            for i, word_data in enumerate(whisper_data["words"]):
                start = word_data["start"]
                end = word_data["end"]
                text = word_data["word"]
                event = pysubs2.SSAEvent(
                    start=pysubs2.make_time(s=start),
                    end=pysubs2.make_time(s=end),
                    text=f"\u202B{text.strip()}\u202C" if config.get("rtl") else text.strip()
                )
                subs.events.append(event)

        elif config.get("karaoke"):
            ass_text = ""
            current_start = whisper_data["words"][0]["start"]
            current_end = whisper_data["words"][-1]["end"]
            for word in whisper_data["words"]:
                word_text = word["word"].strip()
                duration = word["end"] - word["start"]
                ms = int(duration * 100)
                ass_text += f"{{\k{ms}}}{word_text} "

            event = pysubs2.SSAEvent(
                start=pysubs2.make_time(s=current_start),
                end=pysubs2.make_time(s=current_end),
                text=f"\u202B{ass_text.strip()}\u202C" if config.get("rtl") else ass_text.strip()
            )
            subs.events.append(event)

        subs.save(str(ass_path), format="ass")

        with open(vtt_path, "w", encoding="utf-8") as f:
            f.write("WEBVTT\n\n")
            for i, line in enumerate(subs):
                f.write(f"{i+1}\n")
                f.write(f"{line.start.to_time()} --> {line.end.to_time()}\n")
                f.write(f"{line.text}\n\n")
        return

    subs = pysubs2.load(str(srt_path), encoding="utf-8")

    if config.get("rtl"):
        for line in subs:
            line.text = f"\u202B{line.text.strip()}\u202C"

    if config.get("replace_terms"):
        for line in subs:
            for src, dst in config["replace_terms"].items():
                line.text = line.text.replace(src, dst)

    subs.save(str(ass_path), format="ass")

    with open(vtt_path, "w", encoding="utf-8") as f:
        f.write("WEBVTT\n\n")
        for i, line in enumerate(subs):
            f.write(f"{i+1}\n")
            f.write(f"{line.start.to_time()} --> {line.end.to_time()}\n")
            f.write(f"{line.text}\n\n")