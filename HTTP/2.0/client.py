import httpx

if __name__ == '__main__':
    url = 'https://localhost:8001'
    with httpx.Client(http2=True, verify=False) as client:
        response = client.get(url)
        print(f'Status Code: {response.status_code}')
        print(f'HTTP Version: {response.http_version}')
        print(f'Headers: {response.headers}')
        print(f'Body: {response.text}')
