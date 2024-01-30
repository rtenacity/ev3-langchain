import requests

# The URL of the Flask endpoint
url = 'http://127.0.0.1:5000/receive_code'

# The code to be executed
data = {
    'code': """print("Hello, World")"""
}

# Send a POST request
response = requests.post(url, json=data)

# Print the response from the server
print('Response from the server:')
print(response.text)