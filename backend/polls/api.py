from urllib.parse import urlencode, unquote, quote_plus
from urllib.request import urlopen
import json
import xmltodict
from decouple import config

class Api:
    def __init__(self, city, locDate):
        self.serviceKey = config('SERVICE_KEY')
        self.decodedServiceKey = unquote(self.serviceKey, 'UTF-8')
        self.city = city
        self.locDate = locDate

    def getData(self):
        url = 'http://apis.data.go.kr/B090041/openapi/service/RiseSetInfoService/getAreaRiseSetInfo'

        params = '?' + urlencode({quote_plus('serviceKey'):self.decodedServiceKey,
                                quote_plus('locdate'):self.locDate,
                                quote_plus('location'):self.city})
        request = url + params
        response_body = urlopen(request).read()
        decode_data = response_body.decode('utf-8')

        xml_parse = xmltodict.parse(decode_data)
        xml_dict = json.loads(json.dumps(xml_parse))

        return xml_dict['response']['body']['items']['item']
