from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import json
import os

# Генерация ключевой пары
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

# Сериализация и сохранение закрытого ключа
private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

with open(".well-known/private_key.txt", "wb") as private_key_file:
    private_key_file.write(private_pem)

# Получение открытого ключа
public_key = private_key.public_key()

# Сериализация и сохранение открытого ключа
public_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# Формирование массива ключей jwks
jwks = {
    "keys": [
        {
            "kty": "RSA",
            "alg": "RS256",
            "x5c": [public_pem.decode('utf-8')],
        }
    ]
}

# Создание папки .well-known, если она не существует
if not os.path.exists(".well-known"):
    os.mkdir(".well-known")

# Запись jwks в файл
with open(".well-known/jwks.json", "w") as jwks_file:
    json.dump(jwks, jwks_file, indent=4)



"""
Этот скрипт генерирует пару ключей RSA и выводит их в формате JWKS. Вы можете интегрировать этот код в ваш Docker-контейнер и запустить его вместо PHP-скрипта для генерации JWKS. Не забудьте установить библиотеку PyJWT в вашем Docker-контейнере или включить ее в зависимости вашего проекта.
import json
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
import jwt

# Генерация ключей RSA
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)
public_key = private_key.public_key()

# Преобразование ключей в формат JSON Web Key (JWK)
private_jwk = json.dumps(jwt.OctetJWK.from_key(private_key).to_dict())
public_jwk = json.dumps(jwt.OctetJWK.from_key(public_key).to_dict())

# Вывод JWK на экран
print("Private JWKS:")
print(private_jwk)

print("Public JWKS:")
print(public_jwk)

"""
