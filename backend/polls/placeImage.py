import urllib.request
import json
from decouple import config

class PlaceImage():
    def __init__(self, encText):
        self.encText = encText

    def getLink(self):
        NAVER_CLIENT_ID = config('NAVER_CLIENT_ID')
        NAVER_CLIENT_SECRET = config('NAVER_CLIENT_SECRET')
        self.encText = urllib.parse.quote(self.encText)
        url = f"https://openapi.naver.com/v1/search/image?query={self.encText}" \
            f"&display=1&sort=sim"

        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id", NAVER_CLIENT_ID)
        request.add_header("X-Naver-Client-Secret", NAVER_CLIENT_SECRET)
        response = urllib.request.urlopen(request)
        rescode = response.getcode()

        if rescode == 200:
            response_body = response.read()
            response_body = response_body.decode('utf-8')
            res_json = json.loads(response_body)
            link = res_json['items'][0]['link']
            return link
        else:
            print(rescode)