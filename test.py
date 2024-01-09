import http.client

conn = http.client.HTTPConnection("127.0.0.1", 8000)

headersList = {
 "Accept": "*/*",
 "User-Agent": "Thunder Client (https://www.thunderclient.com)" 
}

payload = ""

conn.request("GET", "/get_instructions?user_instr=Drive%20forward%20until%20you%20detect%20an%20object", payload, headersList)
response = conn.getresponse()
result = response.read()

print(result.decode("utf-8"))