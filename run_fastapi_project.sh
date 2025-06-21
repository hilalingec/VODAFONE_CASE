#!/bin/bash

echo "VODAFONE FastAPI Project loading (Linux)..."

# Docker kurulu mu?
if ! command -v docker &> /dev/null
then
    echo "Docker kurulu degil. Docker engine kurun."
    exit 1
fi

#  Docker Engine  calisiyo mu?
if ! docker info > /dev/null 2>&1
then
    echo " Docker servisi calismiyor. Programi sonlandir."
    exit 1
fi

# Proje başlatılıyor
echo "Docker container ayaga kaldiriliyor..."
docker-compose up --build