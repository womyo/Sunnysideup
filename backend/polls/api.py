from urllib.parse import urlencode, unquote, quote_plus
from urllib.request import urlopen
import json
import xmltodict

serviceKey = 'cl47XS7A0i8vg0NZNiXYCR5+9Df0fCXMZ+tyIPdr/va2clSHIMvlnzFeTqrmgZZtO8ARtV2qB8+R8bfVJmB9yQ=='
decodedServiceKey = unquote(serviceKey, 'UTF-8')

def getData(city, locDate):
    url = 'http://apis.data.go.kr/B090041/openapi/service/RiseSetInfoService/getAreaRiseSetInfo'

    params = '?' + urlencode({quote_plus('serviceKey'):decodedServiceKey,
                              quote_plus('locdate'):locDate,
                              quote_plus('location'):city})
    request = url + params
    response_body = urlopen(request).read()
    decode_data = response_body.decode('utf-8')

    xml_parse = xmltodict.parse(decode_data)
    xml_dict = json.loads(json.dumps(xml_parse))

    return xml_dict['response']['body']['items']['item']
