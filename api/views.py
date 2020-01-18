from django.http import HttpResponse
from rest_framework.parsers import FileUploadParser, MultiPartParser, JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from api.image_distance_classifier import ImageDistanceClassifier
from api.image_features_extraction import ImageFeatureExtraction
from api.models import File
from api.serializers import FileSerializer


class ImageView(APIView):
    parser_classes = (FileUploadParser,)

    def post(self, request, *args, **kwargs):
        data = request.FILES
        file_serializer = FileSerializer(data=data)
        if file_serializer.is_valid():
            file_serializer.save()
            saved_file = File.objects.get(id=file_serializer.data['id'])
            features_extractor = ImageFeatureExtraction(saved_file)
            features_extractor.get_features()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageIdView(APIView):
    parser_classes = (JSONParser,)

    def get(self, request, img_id):
        try:
            file = File.objects.get(id=img_id)
            fnc = ImageDistanceClassifier(file)
            return Response({"id": file.id, "name": file.file.name, "url": file.get_url(), "results": fnc.get_results()}, status=status.HTTP_200_OK)
        except File.DoesNotExist:
            return Response({"error": "Le fichier demandé n'existe pas"}, status=status.HTTP_404_NOT_FOUND)
