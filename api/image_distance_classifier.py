from sklearn.metrics.pairwise import cosine_similarity

from api.models import File


class ImageDistanceClassifier:
    file: File

    def __init__(self, file):
        self.file = file

    def get_results(self):
        vectors = self.get_distances()
        results = sorted(vectors.items(), key=lambda x: x[1], reverse=True)
        output = []
        i = 0
        for (k, v) in results:
            if i > 4:
                break
            output.append({
                "url": "ns3017873.ip-149-202-86.eu:8001/" + k,
                "score": v
            })
            i += 1
        return output

    def get_distances(self):
        vector_list = {}
        feature_list = []
        feature_weigth_list = self.file.featureweigth_set.all()
        for ft in feature_weigth_list:
            feature_list.append(ft.feature.label)

        for file in File.objects.filter(indexed=True, featureweigth__feature__label__in=feature_list):
            if file.file.name != self.file.file.name:
                vector_list[file.file.name] = self.file.get_cosine_distance(file)

        return vector_list
