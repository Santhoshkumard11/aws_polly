# FastAPI Polly TTS Service

## Overview
This project is a FastAPI-based application that provides a simple text-to-speech (TTS) service using Amazon Polly. It allows users to synthesize speech from text and play it back directly or fetch the list of available voices supported by Polly.

## Features
- **Text-to-Speech Endpoint**: Convert text to speech using Amazon Polly.
- **Voice Listing**: Retrieve a list of voices available in Amazon Polly.
- **CORS Support**: Allows integration with frontend applications hosted on `http://localhost:3000`.

## Technologies Used
- **FastAPI**: For building the API.
- **Amazon Polly**: For TTS services.
- **Boto3**: AWS SDK for Python to interact with Polly.
- **Uvicorn**: ASGI server for running the FastAPI app.
- **Playsound**: To play synthesized audio locally.

---

## Prerequisites
1. **Python**: Ensure Python 3.8 or higher is installed.
2. **AWS Credentials**: Set up AWS access and secret keys with permissions to use Polly.

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Set Up a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the project root:
```plaintext
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=your_aws_region
```
Replace `your_aws_access_key`, `your_aws_secret_key`, and `your_aws_region` with your AWS credentials and desired region.

### 5. Run the Application
```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

The app will be available at `http://127.0.0.1:8000`.

---

## API Endpoints

### 1. **POST** `/playsound`
Converts text to speech and plays the audio.

#### Request Body (JSON):
```json
{
  "text": "Hello, world!",
  "voice": "Joanna",   // Optional, default: "Joanna"
  "format": "mp3"       // Optional, default: "mp3"
}
```

#### Response:
```json
{
  "message": "Playing audio..."
}
```

### 2. **GET** `/voices`
Fetches a list of all available voices from Amazon Polly.

#### Response:
```json
[
  {
    "Id": "Joanna",
    "Name": "Joanna",
    "LanguageCode": "en-US",
    "Gender": "Female",
    ...
  },
  ...
]
```

---

## CORS Configuration
The app allows requests from `http://localhost:3000` by default. To modify CORS settings, update the `allow_origins` list in the CORS middleware configuration in `app.py`.

---

## Troubleshooting

### Common Errors
- **CORS Errors**: Ensure the frontend's origin is added to the `allow_origins` list.
- **AWS Credentials Issues**: Verify the `.env` file and ensure the credentials are valid and have Polly permissions.

---

## Future Improvements
- Add support for saving synthesized audio files.
- Extend the service to include more Polly features (e.g., SSML).
- Create a frontend interface for easier interaction.

---

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Contributions
Contributions are welcome! Feel free to submit a pull request or open an issue for suggestions or bug reports.

