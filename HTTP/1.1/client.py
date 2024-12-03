import requests

if __name__ == '__main__':
    response = requests.get('http://localhost:8000')
    print(f'Status Code: {response.status_code}')
    print(f'Headers: {response.headers}')
    print(f'Body: {response.text}')
