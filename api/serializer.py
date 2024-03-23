from rest_framework import serializers
from zybal.models import Profile



class ProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', read_only=True)

    class Meta:
        model = Profile
        fields = ['id_user','first_name']