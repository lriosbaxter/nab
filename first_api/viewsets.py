from django.contrib.auth.hashers import make_password
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import User, Folder, Script

from .serializers.first_api_serializers import UserSerializer, \
    FolderSerializer, ScriptSerializer


class UserViewSets(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        request.data['password'] = make_password(request.data['password'])
        return super().create(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        password = request.data['password']
        if password:
            request.data['password'] = make_password(password)
        else:
            request.data['password'] = request.user.password
        return super().update(request, *args, **kwargs)


class FolderViewSets(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer


class ScriptViewSets(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    queryset = Script.objects.all()
    serializer_class = ScriptSerializer
