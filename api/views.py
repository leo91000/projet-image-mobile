from django.http import HttpResponse
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from api.serializers import FileSerializer


class ImageView(APIView):
    parser_classes = (FileUploadParser,)

    def post(self, request, *args, **kwargs):
        data = request.FILES
        file_serializer = FileSerializer(data=data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
