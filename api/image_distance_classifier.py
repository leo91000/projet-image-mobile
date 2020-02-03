from sklearn.metrics.pairwise import cosine_similarity

from api.models import File


class ImageDistanceClassifier:
    file = File()

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
                "url": "/static/" + k,
                "score": v
            })
            i += 1
        return output

    def get_distances(self):
        vector_list = {}

        for file in File.objects.filter(indexed=True):
            if file.file.name != self.file.file.name:
                vector_list[file.file.name] = self.file.get_cosine_distance(file)

        return vector_list
