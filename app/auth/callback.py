import requests

jwt_param = input("Enter JWT parameter: ")  # Здесь вы можете получить значение jwt из URL-параметра или каким-либо другим способом
url = f"http://identity_provider:80/callback?jwt={jwt_param}"

response = requests.get(url)

if response.status_code == 200:
    print(response.text)
else:
    print(f"Error: {response.status_code}")
