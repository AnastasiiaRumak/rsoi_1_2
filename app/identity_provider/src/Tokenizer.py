import jwt
import json
import os
from datetime import datetime, timedelta

class Tokenizer:
    def __init__(self):
        private_key_path = ".well-known/private_key.txt"
        self.private_key = self.load_private_key(private_key_path)

    def load_private_key(self, private_key_path):
        try:
            with open(private_key_path, 'rb') as private_key_file:
                return private_key_file.read()
        except Exception as e:
            print(f"Error loading private key: {e}")
            return None

    def generate_token(self, payload):
        try:
            expiration_time = datetime.utcnow() + timedelta(minutes=120)
            payload['iat'] = datetime.utcnow()
            payload['exp'] = expiration_time
            jwt_token = jwt.encode(payload, self.private_key, algorithm='RS256')
            return jwt_token
        except Exception as e:
            print(f"Error generating token: {e}")
            return None

    def check_token(self, jwt):
        try:
            jwks_path = ".well-known/jwks.json"
            with open(jwks_path, 'r') as jwks_file:
                jwks_data = json.load(jwks_file)
            jwk = jwks_data['keys'][0]['x5c'][0]
            decoded = jwt.decode(jwt, jwk, algorithms=['RS256'])
            return json.dumps(decoded)
        except jwt.ExpiredSignatureError:
            return 'Token expired'
        except jwt.InvalidSignatureError:
            return 'Invalid signature'
        except Exception as e:
            print(f"Error decoding token: {e}")
            return None

if __name__ == '__main__':
    tokenizer = Tokenizer()

    payload = {
        "email": "user@example.com",
        "profile": "user_profile"
    }

    token = tokenizer.generate_token(payload)
    print("Generated Token:")
    print(token)

    decoded_token = tokenizer.check_token(token)
    print("\nDecoded Token:")
    print(decoded_token)
