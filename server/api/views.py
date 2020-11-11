import json
import os
import traceback
import uuid
from mimetypes import guess_type
from shutil import copyfile

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import redirect
from django.views.generic import ListView
from django.views.generic.base import View
from rest_framework.parsers import FileUploadParser, MultiPartParser, JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from api.image_distance_classifier import ImageDistanceClassifier
from api.image_features_extraction import ImageFeatureExtraction
from api.models import File, FeatureWeigth, SearchResults
from api.serializers import FileSerializer

from image_mobile.settings import IMAGE_ROOT, MEDIA_ROOT, UPLOADED_IMAGE_ROOT


class ImageView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, *args, **kwargs):
        try:
            data = request.FILES['file']
            index_image = \
                request.data['index'] == '1' or \
                request.data['index'] == 'True' or \
                request.data['index'] == 'true'
            if isinstance(data, InMemoryUploadedFile):
                if not os.path.exists(UPLOADED_IMAGE_ROOT):
                    os.makedirs(UPLOADED_IMAGE_ROOT)

                file_name = data.name
                if file_name.endswith('"'):
                    file_name = file_name[:-1]
                file_path = os.path.join(UPLOADED_IMAGE_ROOT, str(uuid.uuid4()))
                with default_storage.open(file_path, "wb+") as destination:
                    for chunk in data.chunks():
                        destination.write(chunk)

                file = File()
                file.file_path = file_path
                file.file_name = file_name
                file.indexed = index_image
                file.save()
                features_extractor = ImageFeatureExtraction(file)
                features_extractor.get_features()
                fnc = ImageDistanceClassifier(file)
                search_results = SearchResults()
                search_results.results = json.dumps(
                    {"id": file.id, "name": file.file_name, "url": file.get_url(), "results": fnc.get_results()})
                search_results.file = file
                search_results.save()
                return Response({"id": file.id, "indexed": file.indexed, "file": {"name": file.file_name}},
                                status=status.HTTP_201_CREATED)

            else:
                return Response({"file": ["This field is required", "This field should be an uploaded file"]},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e.args[0])
            return Response({"error": e.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ImageIdView(APIView):
    parser_classes = (JSONParser,)

    def get(self, request, img_id):
        try:
            file = File.objects.get(id=img_id)
            if file.searchresults_set.all().exists():
                search_results = file.searchresults_set.first()
                data = json.loads(search_results.results)
                data['feedback'] = search_results.feedback
                return Response(data, status=status.HTTP_200_OK)
            else:
                fnc = ImageDistanceClassifier(file)
                return Response(
                    {"id": file.id, "name": file.file_name, "url": file.get_url(), "results": fnc.get_results()},
                    status=status.HTTP_200_OK)
        except File.DoesNotExist:
            return Response({"error": "Le fichier demandé n'existe pas"}, status=status.HTTP_404_NOT_FOUND)


class ImageFileView(View):
    def get(self, request, img_id, img_name):
        try:
            print("View image", img_id, img_name)
            file = File.objects.get(id=img_id)
            if file:
                if file.file_name != img_name:
                    return redirect(file.get_url())

                try:
                    with open(file.get_path(), "rb") as f:
                        file_data = f.read()

                    response = HttpResponse(file_data, content_type=guess_type(file.file_name)[0])
                    response['Content-Disposition'] = 'attachment; filename="' + file.file_name + '"'
                except IOError:
                    response = HttpResponseNotFound("<h1>Le fichier demandé n'existe pas (IOError)</h1>")
            else:
                response = HttpResponseNotFound("<h1>Le fichier demandé n'existe pas</h1>")
        except File.DoesNotExist:
            response = HttpResponseNotFound("<h1>Le fichier demandé n'existe pas</h1>")
        return response


class FeedbackView(APIView):
    parser_classes = (JSONParser,)

    def post(self, request, img_id):
        file = File.objects.get(id=img_id)
        if file.searchresults_set.all().exists():
            search_results = file.searchresults_set.first()
            data = request.data
            data['img_id'] = img_id
            search_results.feedback = data['relevance']
            search_results.save()
            return Response(data, status=status.HTTP_200_OK)
        else:
            return HttpResponseNotFound({'error': 'L\'ID ' + img_id + 'n\'existe pas en BDD, vérifiez votre requête'})


class IndexerView(APIView):
    parser_classes = (JSONParser,)

    @staticmethod
    def get():
        try:
            FeatureWeigth.objects.filter(file__indexed=True).delete()
            File.objects.filter(indexed=True).delete()
            with open(os.path.join(os.path.join(IMAGE_ROOT, "Eval"), "list_eval_partition.txt"), "r") as f:
                partition_file = f.readlines()[2:]
                for line in partition_file:
                    path = line.split(" ", 1)[0].replace('/', os.sep)
                    file_path = os.path.join(IMAGE_ROOT, path)
                    filename = os.path.basename(file_path)
                    file_model = File()
                    file_model.file_name = filename
                    file_model.file_path = file_path
                    file_model.indexed = True
                    file_model.save()
                    features_extractor = ImageFeatureExtraction(file_model)
                    features_extractor.get_features()
                    print("Analyzed " + path)
            return Response({"success": True}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"success": False, "message": e.args[0]})
