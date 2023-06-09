# Use an official Python runtime as the base image
FROM python:3.11-slim-bullseye
LABEL authors="I-Kozhin"

# нужен чтобы логи нормально из контейнера вылезали
# тоже можно поставить, все равно кеш питон кода в контейнере лишь место лишнее занимать будет
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update && apt-get install

RUN apt-get install -y \
  dos2unix \
  libpq-dev \
  libmariadb-dev-compat \
  libmariadb-dev \
  gcc \
  && apt-get clean

RUN python -m pip install --upgrade pip

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt ./

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project to the container
COPY . .

# Expose the port on which the application will run
EXPOSE 8000