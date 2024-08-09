from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class HelloWorldView(APIView):
    def get(self, request):
        response = {'data': 'Hello, world!'}
        return Response(data=response, status=status.HTTP_200_OK)

    def post(self, request):
        response = {'data': 'Hello, world!'}
        return Response(data=response, status=status.HTTP_200_OK)
