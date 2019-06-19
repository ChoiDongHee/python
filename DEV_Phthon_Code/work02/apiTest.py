
import requests
import urllib
import json
import http

def smartPush(userSaid):
    conn = http.client.HTTPSConnection("spisdev.paran.com")
    payload = "{\n  \"said\": [\n    \""+userSaid+"\"\n  ]\n}\n"
    print(payload)
    headers = {
        'content-type': "application/json",
        'x-auth-token': "1e4dfe44-d7e9-dce2-1d5a-0a46-6ad3-5b57-3ab9-05a3-273f-38a76abddc3ead3d4c20",
        'cache-control': "no-cache",
        'postman-token': "ac070378-ba5b-ffe5-34cb-28ad12a816c9"
    }

    conn.request("POST", "/sprtm/message/send/201810311011", payload, headers)

    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))


smartPush("TT181220011")
