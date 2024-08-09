import re

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from first_api.models import Script
from tools.django_tools import GeneralModel
from first_api.serializers.first_api_serializers import ScriptSerializer
from tools.repository_tools import Repository


class ContentCodeView(APIView):
    def post(self, request):
        repository_name = request.data.get('repository_name')
        script_name = request.data.get('py_archive_name')
        script_content = Repository.get_script_content(repository_name,
                                                       script_name)
        response = {"Script_Data": script_content}
        return Response(data=response,
                        status=status.HTTP_200_OK)
