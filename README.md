# Web User Music Service

This Python-based project provides a web service for music file processing and user management, leveraging PostgreSQL for data storage. The service allows users to upload .wav files, converts them into .mp3 format, and stores them in a PostgreSQL database.

## Features

  * Accepts POST requests for creating users, which includes generating a unique user identifier and a UUID access token.
  * Accepts POST requests for uploading .wav files, which includes converting the file to .mp3 format, generating a unique UUID for the file, and storing it in the PostgreSQL database.
  * Returns the unique user identifier and access token for user creation requests.
  * Returns a URL for downloading the .mp3 file for upload requests. The URL is in the format `http://host:port/record?id=record_id&user=user_id`.
  * Accepts GET requests for downloading the .mp3 files using the provided URL.
  * Handles various error scenarios during the request execution and returns the corresponding HTTP status.
  * Supports data persistence using Docker volumes.

## Installation

  1. Clone the repository: 

        git clone https://github.com/I-Kozhin/py-web-user-music

  2. Navigate to the project directory: 

        cd py-web-user-music

  3. Build the Docker image and start the containers: 

        docker-compose up -d

  4. The service should now be running on `http://localhost:8000`. You can access the API using your preferred API testing tool (e.g., curl, Postman).

## API Usage
Since the program generates unique access tokens for users and unique IDs for audio recordings, an example in general form will be given here. And then an example will be given with the data that I got during testing.

Send a POST request to `http://localhost:8000/user` with the following JSON payload to create a user:

    {
    "username": "Ivan"
    }

Send a POST request to `http://localhost:8000/record` with a unique user identifier, access token, and a .wav file to upload a music file.

Use the GET request to `http://host:port/record?id=record_id&user=user_id` to download the .mp3 file.

Example with my test data (I am running a program on a linux VM). VM_ip is just an ip address of my VM:

Send a POST user request
Request URL:

    http://VM_ip:8000/create-user/?user_name=Ivan
Response:
   
    {
    "user_id": 12,
    "user_token": "e990beb2-60fc-4b35-91f7-1898bda7445f"
    }

Send a POST audio request
Request URL without request body:

    http://VM_ip:8000/add-audio/?user_id=8&user_token=4cd7c514-19dd-4155-baad-fa82130e6b5f
Response:
   
    {
    "http://VM_ip:8000/record?audio_id=29d7217e-0fc0-4206-8f26-962fc11440f7&user_id=8"
    }

Send a GET audio request:
Request URL:

    http://VM_ip:8000/record?audio_id=1bddb288-2942-42fd-85ed-94c50abd90e6&user_id=8

As response the audio file in mp3 format will be downloaded by itself or will be downloaded when the user clicks on the download link in the GUI.

## Dependencies

  * Python 3
  * FastAPI
  * SQLAlchemy
  * Docker
  * PostgreSQL
  * Any audio processing library for .wav to .mp3 conversion (ffmpeg works for me)
  * asyncpg
  * uvicorn

## Contributing

Contributions to this project are welcome! If you find any issues or have suggestions for improvements, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License.