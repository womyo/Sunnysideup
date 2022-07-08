from re import L
from rest_framework.response import Response
from rest_framework import viewsets
from .api import Api
from .predictRiseSet import PredictRiseSet
from rest_framework.views import APIView
from .models import Rise, Set
from .serializer import RiseSerializer, SetSerializer

class RiseSetView(APIView):
    def get(self, request, post_pk, pk, format=None):
        api = Api(post_pk, pk)
        res = api.getData()
        
        return Response(data=res)

class PredictView(APIView):
    def get(self, request, pk_1, pk_2, pk_3, pk_4):
        predictRiseSet = PredictRiseSet(pk_1, pk_2, pk_3, pk_4)
        sunRise, sunSet = predictRiseSet.calculate()

        res = {'sunrise': sunRise, 'sunset': sunSet}
        return Response(data=res)

class RiseView(APIView):
    def post(self, request):
        place_serializer = RiseSerializer(data=request.data)

        if place_serializer.is_valid():
            place_serializer.save()
            return Response(place_serializer.data)
        else:
            return Response(place_serializer.errors)
    
    def get(self, request):
        queryset = Rise.objects.all()
        serialized_rise = RiseSerializer(queryset, many=True)
        return Response(data=serialized_rise.data)

class SetView(APIView):
    def post(self, request):
        place_serializer = SetSerializer(data=request.data)

        if place_serializer.is_valid():
            place_serializer.save()
            return Response(place_serializer.data)
        else:
            return Response(place_serializer.errors)

    def get(self, request):
        queryset = Set.objects.all()
        serialized_set = SetSerializer(queryset, many=True)
        return Response(data=serialized_set.data)