import re
import os
import sys
from dotenv import load_dotenv
import urllib.request
import json
load_dotenv()
client_id = os.getenv("PAPAGO_CLIENT_ID") # 개발자센터에서 발급받은 Client ID 값
client_secret = os.getenv("PAPAGO_CLIENT_SECRET") # 개발자센터에서 발급받은 Client Secret 값
def translate(text):
    encText = urllib.parse.quote(text)
    data = "source=ko&target=en&text=" + encText
    url = "https://openapi.naver.com/v1/papago/n2mt"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        result = json.loads(response_body.decode('utf-8'))
        return result["message"]["result"]["translatedText"]
    else:
        return "Error Code:" + rescode
def contains_hangul(text):
    hanCount = len(re.findall(u'[\u3130-\u318F\uAC00-\uD7A3]+', text))
    return hanCount > 0