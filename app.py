from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from pipeline import run_pipeline, PipelineError

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RecipeRequest(BaseModel):
    youtube_url: str
    servings: int


# Maps a failed pipeline stage to a meaningful HTTP status code.
STAGE_STATUS_CODES = {
    "download": 422,            # bad/unsupported URL, private video, etc.
    "transcription": 502,       # upstream Sarvam failure
    "extraction": 502,          # upstream Gemini failure / empty result
    "quantity_generation": 502, # upstream Gemini failure
}


@app.post("/process_recipe")
def process_recipe(request: RecipeRequest):

    try:
        return run_pipeline(request.youtube_url, request.servings)

    except PipelineError as e:
        raise HTTPException(
            status_code=STAGE_STATUS_CODES.get(e.stage, 500),
            detail=f"{e.stage} failed: {e.message}",
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}",
        )
