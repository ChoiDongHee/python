import http.client

conn = http.client.HTTPSConnection("spisdev.paran.com")

payload = "{\n  \"said\": [\n    \"TT181220012\"\n  ]\n}\n"

headers = {
    'content-type': "application/json",
    'x-auth-token': "1e4dfe44-d7e9-dce2-1d5a-0a46-6ad3-5b57-3ab9-05a3-273f-38a76abddc3ead3d4c20",
    'cache-control': "no-cache",
    'postman-token': "db7ae4e8-a3ae-3786-6e2f-a92615c308e3"
    }

conn.request("POST", "/sprtm/message/send/201811081001", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))