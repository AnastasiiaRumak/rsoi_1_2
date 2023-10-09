# Используйте базовый образ Python
FROM python:3.9

# Устанавливаем рабочую директорию
WORKDIR /app

RUN  pip install --upgrade pip

# Устанавливаем необходимые зависимости для вашего Python-приложения
RUN apt-get update && apt-get install -y \
    libpq-dev \
    zlib1g-dev \
    libzip-dev \
    unzip

# Установите необходимые Python-библиотеки с помощью pip
RUN pip install \
    psycopg2-binary \
    redis \
    confluent-kafka


# Другие инструкции Dockerfile для вашего Python-контейнера

# Копируем код микросервисов в контейнер
COPY . /app
