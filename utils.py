import json
import os


def load_transcript(output_folder):
    """
    Load transcript JSON files belonging ONLY to output_folder.

    IMPORTANT: output_folder must be a request-scoped, unique folder
    (e.g. output/<request_id>/transcript_raw) created fresh for this
    request. Never pass a shared/global folder path here — doing so is
    exactly how a previous recipe's transcript gets reused.
    """
    if not os.path.isdir(output_folder):
        raise FileNotFoundError(
            f"Transcript output folder not found: {output_folder}"
        )

    transcript = ""
    found_any = False

    for file in sorted(os.listdir(output_folder)):

        if file.endswith(".json"):

            found_any = True

            with open(
                os.path.join(output_folder, file),
                encoding="utf-8"
            ) as f:

                data = json.load(f)

                transcript += data["transcript"] + "\n"

    if not found_any:
        raise FileNotFoundError(
            f"No transcript JSON files found in {output_folder}. "
            "Refusing to fall back to any other folder."
        )

    return transcript.strip()


def save_json(data, path):
    """Save data as JSON to path, creating parent directories if needed."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
