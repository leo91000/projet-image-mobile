import os
import uuid
from shutil import copyfile

from django.http import HttpResponse
from rest_framework.parsers import FileUploadParser, MultiPartParser, JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from api.image_distance_classifier import ImageDistanceClassifier
from api.image_features_extraction import ImageFeatureExtraction
from api.models import File, FeatureWeigth
from api.serializers import FileSerializer

from image_mobile.settings import IMAGE_ROOT, MEDIA_ROOT


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


class IndexerView(APIView):
    parser_classes = (JSONParser,)

    def get(self):
        try:
            FeatureWeigth.objects.filter(file__indexed=True).delete()
            File.objects.filter(indexed=True).delete()
            with open(os.path.join(os.path.join(IMAGE_ROOT, "Eval"), "list_eval_partition.txt"), "r") as f:
                partition_file = f.readlines()[2:]
                for line in partition_file:
                    path = line.split(" ", 1)[0].replace('/', os.sep)
                    file_path = os.path.join(IMAGE_ROOT, path)
                    filename = os.path.basename(file_path)
                    filename_no_extension, file_extension = os.path.splitext(filename)
                    unique_name = filename_no_extension + "_" + str(uuid.uuid4()) + file_extension
                    generated_path = os.path.join(MEDIA_ROOT, unique_name)
                    copyfile(file_path, generated_path)
                    file_model = File()
                    file_model.file.name = unique_name
                    file_model.indexed = True
                    file_model.save()
                    features_extractor = ImageFeatureExtraction(file_model)
                    features_extractor.get_features()
            return Response({"success": True}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"success": False, "message": e.args[0]})







