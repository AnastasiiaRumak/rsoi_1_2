import requests

profile_param = input("Enter profile parameter: ")  # Замените на ваш способ получения параметра profile
email_param = input("Enter email parameter: ")      # Замените на ваш способ получения параметра email

url = f"http://identity_provider:80/autorize?profile={profile_param}&email={email_param}"

response = requests.get(url)

if response.status_code == 200:
    print(response.text)
else:
    print(f"Error: {response.status_code}")
