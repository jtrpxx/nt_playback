# serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import MainDatabase,UserAuth,UserLog,SetAudio,Department,UserProfile,UserGroup,UserTeam

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name_th', 'name_en']

class MainDatabaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainDatabase
        fields = '__all__'

class UserAuthSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    maindatabase = MainDatabaseSerializer(read_only=True)

    class Meta:
        model = UserAuth
        fields = ['id', 'user', 'maindatabase', 'privilege']

class UserLogSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    audiofile_id = serializers.IntegerField(source='audiofile.id', read_only=True)

    class Meta:
        model = UserLog
        fields = ['id', 'user', 'action', 'timestamp', 'detail', 'ip_address', 'audiofile_id']

class SetAudioSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = SetAudio
        fields = ['id', 'user', 'audio_path', 'create_at', 'update_at']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    department = DepartmentSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'department', 'user_code', 'phone', 'create_at', 'update_at']

class UserGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGroup
        fields = '__all__'

class UserTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTeam
        fields = '__all__'

