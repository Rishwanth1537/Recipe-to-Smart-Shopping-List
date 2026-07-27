import os
import shutil
import uuid

import yt_dlp

from transcribe import SarvamTranscriber
from utils import load_transcript, save_json
from ingredient_extractor import extract_ingredients
from merge import merge_duplicates
from quantity_generator import generate_quantities

BASE_OUTPUT_FOLDER = "output"

# Stage output files kept for debugging after each request completes.
DEBUG_FILES = ("transcript.json", "ingredients.json", "shopping_list.json")


class PipelineError(Exception):
    """
    Raised when a specific pipeline stage fails, so app.py can translate
    it into a meaningful HTTP status/message instead of a generic 500.
    """

    def __init__(self, stage, message):
        self.stage = stage
        self.message = message
        super().__init__(f"[{stage}] {message}")


def _download_audio(youtube_url, request_dir):

    output_template = os.path.join(request_dir, "audio.%(ext)s")

    ydl_opts = {
        "format": "bestaudio",
        "outtmpl": output_template,
        "quiet": False,
        "noplaylist": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "0",
            }
        ],
        "postprocessor_args": ["-ar", "16000", "-ac", "1"],
    }

    print("=" * 70)
    print("STEP 1 : Downloading YouTube Audio")
    print("=" * 70)

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=True)
    except Exception as e:
        raise PipelineError("download", str(e))

    audio_path = os.path.join(request_dir, "audio.wav")

    if not os.path.exists(audio_path):
        raise PipelineError("download", "Downloaded audio file was not found on disk.")

    print("Download Complete:", audio_path)

    return info, audio_path


def _transcribe(audio_path, request_dir):

    print("=" * 70)
    print("STEP 2 : Transcribing using Sarvam")
    print("=" * 70)

    # Request-scoped transcript folder — never shared across requests.
    transcript_dir = os.path.join(request_dir, "transcript_raw")

    try:
        transcriber = SarvamTranscriber()
        transcriber.transcribe(audio_path, transcript_dir)
        transcript = load_transcript(transcript_dir)
    except Exception as e:
        raise PipelineError("transcription", str(e))

    print("Transcript Length :", len(transcript))

    return transcript


def _extract_ingredients(recipe_title, transcript):

    print("=" * 70)
    print("STEP 3 : Extracting Ingredients (single Gemini call)")
    print("=" * 70)

    try:
        result = extract_ingredients(recipe_title, transcript)
    except Exception as e:
        raise PipelineError("extraction", str(e))

    ingredients = result.get("ingredients", [])

    if not ingredients:
        raise PipelineError(
            "extraction",
            "No ingredients could be extracted from the transcript."
        )

    print(f"Found {len(ingredients)} ingredients")

    return ingredients


def run_pipeline(youtube_url, servings):
    """
    Full request-scoped pipeline. Every call gets its own UUID folder, so
    two concurrent requests (or a retried request) can never read each
    other's transcript, ingredients, or shopping list.
    """

    request_id = str(uuid.uuid4())
    request_dir = os.path.join(BASE_OUTPUT_FOLDER, request_id)
    os.makedirs(request_dir, exist_ok=True)

    try:
        info, audio_path = _download_audio(youtube_url, request_dir)
        recipe_title = info["title"]

        transcript = _transcribe(audio_path, request_dir)
        save_json(
            {"transcript": transcript},
            os.path.join(request_dir, "transcript.json")
        )

        all_ingredients = _extract_ingredients(recipe_title, transcript)

        print("=" * 70)
        print("STEP 4 : Merging Ingredients")
        print("=" * 70)

        merged_ingredients = merge_duplicates(all_ingredients)
        save_json(
            {"ingredients": merged_ingredients},
            os.path.join(request_dir, "ingredients.json")
        )

        print(f"Total Extracted : {len(all_ingredients)}")
        print(f"Unique Ingredients : {len(merged_ingredients)}")

        print("=" * 70)
        print("STEP 5 : Generating Shopping Quantities")
        print("=" * 70)

        try:
            shopping_list = generate_quantities(recipe_title, servings, merged_ingredients)
        except Exception as e:
            raise PipelineError("quantity_generation", str(e))

        save_json(shopping_list, os.path.join(request_dir, "shopping_list.json"))

        print("=" * 70)
        print("Workflow Completed Successfully")
        print("=" * 70)

        return {
            "status": "success",
            "recipe_name": recipe_title,
            "duration": info.get("duration"),
            "people": servings,
            "shopping_list": shopping_list["ingredients"],
        }

    finally:
        _cleanup(request_dir)


def _cleanup(request_dir):
    """
    Remove bulky temp files (raw audio, raw Sarvam job output) after the
    request completes, keeping only the three debug JSON files, per
    requirement #15.
    """
    if not os.path.isdir(request_dir):
        return

    for name in os.listdir(request_dir):
        if name in DEBUG_FILES:
            continue

        path = os.path.join(request_dir, name)

        if os.path.isdir(path):
            shutil.rmtree(path, ignore_errors=True)
        else:
            try:
                os.remove(path)
            except OSError:
                pass
