from rest_framework import serializers
from api.models import File


class FileSerializer(serializers.ModelSerializer):
    file = serializers.FileField(use_url=False)

    class Meta:
        model = File
        fields = '__all__'
