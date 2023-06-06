# py-web-user-music
This is the web service that creates a user, saves an audio recording in wav format, converts it to mp3 format and writes it to a database and provides a link to download the audio recording.


### поднятие инфраструктуры
    docker-compose -p web-databeses -f docker-compose.yml up user-db
    docker-compose -p test-db -f docker-compose.yml up postgres-db 

    uvicorn app.main:app --host 0.0.0.0 --reload