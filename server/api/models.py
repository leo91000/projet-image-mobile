import os

import numpy as np
from django.db import models
from sklearn.metrics.pairwise import cosine_distances, cosine_similarity

from image_mobile.settings import MEDIA_ROOT, STATIC_URL


class Feature(models.Model):
    model_id = models.TextField(unique=True, max_length=512)
    label = models.TextField(max_length=512)

    def __str__(self):
        return self.label


class File(models.Model):
    file = models.ImageField(blank=False, null=False)
    indexed = models.BooleanField(null=False)

    def __str__(self):
        return self.file.name

    def get_path(self):
        return os.path.join(MEDIA_ROOT, self.file.name)

    def get_url(self):
        return "ns3017873.ip-149-202-86.eu:8001/" + self.file.name

    def get_dictionary(self):
        dictionary = {}
        for feature_weight in self.featureweigth_set.all():
            dictionary[feature_weight.feature.label] = feature_weight.probability
        return dictionary

    def get_cosine_distance(self, file):
        dict1 = self.get_dictionary()
        dict2 = file.get_dictionary()

        dict1_missing = list(set(dict2.keys() - set(dict1.keys())))
        dict2_missing = list(set(dict1.keys() - set(dict2.keys())))

        for i in dict1_missing:
            dict1[i] = 0
        for i in dict2_missing:
            dict2[i] = 0
        vec1 = []
        vec2 = []
        for i in dict1.keys():
            vec1.append(dict1[i])
            vec2.append(dict2[i])

        return cosine_similarity(np.array(vec1).reshape(1, -1), np.array(vec2).reshape(1, -1))[0][0]


class FeatureWeigth(models.Model):
    feature = models.ForeignKey(Feature, on_delete=models.PROTECT)
    probability = models.FloatField()
    file = models.ForeignKey(File, on_delete=models.PROTECT)


class SearchResults(models.Model):
    file = models.ForeignKey(File, on_delete=models.PROTECT)
    results = models.TextField(unique=True, max_length=4096)
