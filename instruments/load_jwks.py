import os
import requests

# Проверяем наличие директории .well-known и создаем ее, если она отсутствует
if not os.path.exists(".well-known"):
    os.mkdir(".well-known")

# Отправляем GET-запрос для получения JWKS и сохраняем его в файл .well-known/jwks.json
jwks_url = "http://identity_provider:80/.well-known/jwks.json"
response = requests.get(jwks_url)

if response.status_code == 200:
    with open(".well-known/jwks.json", "wb") as jwks_file:
        jwks_file.write(response.content)
        print("JWKS успешно сохранен в .well-known/jwks.json")
else:
    print(f"Ошибка при получении JWKS: {response.status_code}")
