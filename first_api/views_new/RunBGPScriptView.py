
from rest_framework.response import Response
from rest_framework.views import APIView
from first_api.models import Script

from tools.django_tools import GeneralModel
from tools.netmiko_tools import Device
from tools.archives_tools import ArchiveTools
from ..serializers.first_api_serializers import ScriptSerializer


class RunBgpScriptView(APIView):
    def post(self, request, pk):
        script = GeneralModel.filter_object_per_model(Script, pk)
        script_serializer = ScriptSerializer(script).data
        device_dictionary = Device.create_device_dictionary(request.data)

        folder_name = script_serializer.get('repository_name')
        archive_name = script_serializer.get('py_archive_name')
        script_run = ArchiveTools.archive_search(folder_name, archive_name,
                                                 device_dictionary)
        print(script_run)
        return Response(script_run)
