from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
import os
from playsound import playsound
from tempfile import gettempdir
import logging

logger = logging.getLogger(__name__)

app = FastAPI()

# # Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://main.d2d9e9l443ymte.amplifyapp.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Initialize Polly client
session = Session(
    region_name=os.environ.get("AWS_REGION"),
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
)
polly = session.client("polly")


class Commentary(BaseModel):
    text: str
    voice: str = "Matthew"


class PeopleGroup(BaseModel):
    male: Commentary
    female: Commentary


class SpeechRequest(BaseModel):
    commentary_text: PeopleGroup
    format: str = "mp3"


@app.post("/playsound")
async def synthesize_speech(request: SpeechRequest):
    """
    Endpoint to synthesize speech using Amazon Polly.
    Expects JSON payload with 'text' and optionally 'voice' and 'format'.
    """
    logger.info("Received request to speak")
    try:
        for item in [request.commentary_text.male, request.commentary_text.female]:
            if not (item.text or item.text.__len__()):
                raise HTTPException(
                    status_code=400, detail="Text is required for speech synthesis"
                )

            # Call Amazon Polly to synthesize speech
            response = polly.synthesize_speech(
                Text=item.text,
                OutputFormat=request.format,
                VoiceId=item.voice,
                Engine="neural",
            )

            # Save audio to a temporary file
            temp_dir = gettempdir()
            output_file = os.path.join(temp_dir, f"output.{request.format}")

            with open(output_file, "wb") as file:
                file.write(response["AudioStream"].read())

            playsound(output_file)

        return {"message": "Playing audio..."}

    except (BotoCoreError, ClientError) as error:
        raise HTTPException(status_code=500, detail=str(error))


@app.get("/voices")
async def get_voices():
    """
    Endpoint to list all available voices from Amazon Polly.
    """
    try:
        response = polly.describe_voices()
        voices = response.get("Voices", [])
        return voices
    except (BotoCoreError, ClientError) as error:
        raise HTTPException(status_code=500, detail=str(error))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
