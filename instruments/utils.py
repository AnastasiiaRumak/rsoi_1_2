import requests
import json
import jwt
import os
from pykafka import KafkaClient

# Функция для проверки здоровья сервиса
def check_health(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except Exception as e:
        raise RuntimeError("kekw")

# Функция для проверки здоровья списка сервисов
def services_is_running(services):
    for domain in services:
        health_url = f"http://{domain}:80/manage/health"
        if check_health(health_url) != "200 ОК":
            raise RuntimeError("kekw")

# GET-запрос
def curl(url, head_vars=None):
    parsed_url = url.split("://")[1]
    domain = parsed_url.split(":")[0]
    health_url = f"http://{domain}:80/manage/health"

    if check_health(health_url) != "200 ОК":
        error = ""
        if domain == "rating_system":
            error = "Bonus Service unavailable"
        raise RuntimeError(error)

    headers = head_vars or {}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text

# POST-запрос
def curl_post(url, post_vars="", head_vars=None, timeout=0):
    parsed_url = url.split("://")[1]
    domain = parsed_url.split(":")[0]
    health_url = f"http://{domain}:80/manage/health"

    if check_health(health_url) != "200 ОК":
        error = ""
        if domain == "rating_system":
            error = "Bonus Service unavailable"
        raise RuntimeError(error)

    headers = head_vars or {}
    headers['Content-Type'] = 'application/json'
    headers['Content-Length'] = str(len(post_vars))

    response = requests.post(url, data=post_vars, headers=headers, timeout=timeout)
    response.raise_for_status()
    return response.text

# Проверить массив на наличие null элементов
def validate(data, func, err_code):
    result = {}
    for key, value in data.items():
        result.update(func(key, value, "variable isnt set"))
    if result:
        return json.dumps(result), err_code

# Проверка значения на null
def validate_null(key, value, message):
    if value is not None:
        return {}
    return {key: message}

# Преобразование JSON в UTF-8
def norm_json_str(data):
    data = data.encode('utf-8').decode('unicode_escape')
    return data

# Функция для сохранения статистики в Kafka
def save_statistic(message):
    try:
        token = os.environ.get('token') or ""
        jwks = json.load(open(".well-known/jwks.json"))
        jwk = jwks['keys'][0]['x5c'][0]
        decoded = jwt.decode(token, jwk, algorithms=['RS256'])
        username = decoded['profile']
    except Exception:
        username = '__Unauthorized'

    message_data = {
        'message': message,
        'service': os.environ['HTTP_HOST'],
        'token': username,
    }
    message_json = json.dumps(message_data)

    client = KafkaClient(hosts="kafka:9092")
    topic = client.topics['logs']
    producer = topic.get_sync_producer()
    producer.produce(message_json.encode('utf-8'))

# Проверка здоровья сервиса перед выполнением кода
if __name__ != "__main__":
    health_url = "http://localhost:80/manage/health"
    if check_health(health_url) != "200 ОК":
        print("Service is not healthy!")
        exit()

# Ваш кодыыыыыыыыыыыы