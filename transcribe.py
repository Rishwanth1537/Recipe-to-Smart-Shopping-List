from sarvamai import SarvamAI
import os


class SarvamTranscriber:

    def __init__(self):

        self.client = SarvamAI(
            api_subscription_key=os.getenv("SARVAM_API_KEY")
        )

    def transcribe(self, audio_path, output_dir):
        """
        Transcribe audio_path with Sarvam and write results into output_dir.

        output_dir MUST be a unique, request-scoped folder created by the
        caller (see pipeline.py). This function never creates or falls
        back to a shared/global "output" folder, so results from one
        request can never bleed into another.
        """

        os.makedirs(output_dir, exist_ok=True)

        print("=" * 60)
        print("Creating Sarvam Batch Job...")
        print("=" * 60)

        job = self.client.speech_to_text_job.create_job(
            model="saaras:v3",
            mode="transcribe",
            language_code="unknown"
        )

        print("Uploading Audio...")
        job.upload_files(
            file_paths=[audio_path]
        )

        print("Starting Job...")
        job.start()

        print("Waiting for transcription...")
        job.wait_until_complete(
            poll_interval=5,
            timeout=1800
        )

        print("Checking Results...")

        results = job.get_file_results()

        print(results)

        if len(results["successful"]) == 0:
            raise Exception("Sarvam failed to transcribe audio.")

        print("Downloading Transcript...")

        job.download_outputs(
            output_dir=output_dir
        )

        print("Done.")

        return output_dir
