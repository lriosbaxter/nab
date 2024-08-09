from first_api.models import User, Folder, Script

from rest_framework import serializers


class ScriptSerializer(serializers.ModelSerializer):

    class Meta:
        model = Script
        fields = '__all__'


class FolderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Folder
        fields = '__all__'


class RenderFolderSerializer(serializers.ModelSerializer):
    scripts = ScriptSerializer(many=False, required=False)

    class Meta:
        model = Folder
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        scripts = Script.objects.filter(source_folder_id=instance.id)
        users = User.objects.filter(user_id=instance)
        serialized_users = UserSerializer(users, many=True).data
        serialized_scripts = ScriptSerializer(scripts, many=True).data
        data['scripts'] = serialized_scripts
        data['users'] = serialized_users
        return data


class UserSerializer(serializers.ModelSerializer):
    source_folders = FolderSerializer(many=True, required=False)

    class Meta:
        model = User
        fields = '__all__'

