from rest_framework.response import Response
from rest_framework import viewsets
from .api import getData
from rest_framework.views import APIView

class RiseSetView(APIView):
    def get(self, request, post_pk, pk, format=None):
        res = getData(post_pk, pk)
        
        return Response(data=res)
