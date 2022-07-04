from re import L
from rest_framework.response import Response
from rest_framework import viewsets
from .api import Api
from .predictRiseSet import PredictRiseSet
from rest_framework.views import APIView

class RiseSetView(APIView):
    def get(self, request, post_pk, pk, format=None):
        api = Api(post_pk, pk)
        res = api.getData()
        
        return Response(data=res)

class PredictView(APIView):
    def get(self, request):
        predictRiseSet = PredictRiseSet(2022,7,5,127)
        sunRise, sunSet = predictRiseSet.calculate()

        res = {'sunrize': sunRise, 'sunset': sunSet}
        return Response(data=res)