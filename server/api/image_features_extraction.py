import numpy as np
from keras.preprocessing import image
from keras.applications.vgg16 import VGG16, preprocess_input, decode_predictions

from api.models import File, Feature, FeatureWeigth


class ImageFeatureExtraction:
    file = File()
    model = VGG16(weights='imagenet', include_top=True)

    def __init__(self, file):
        self.file = file

    def get_features(self):
        img = image.load_img(self.file.get_path(), target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        predictions = decode_predictions(self.model.predict(x))[0]

        for prediction in predictions:
            try:
                feature = Feature.objects.get(model_id=prediction[0])
            except Feature.DoesNotExist:
                feature = Feature()
                feature.model_id = prediction[0]
                feature.label = prediction[1]
                feature.save()

            feature_weight = FeatureWeigth()
            feature_weight.feature = feature
            feature_weight.file = self.file
            feature_weight.probability = prediction[2]
            feature_weight.save()

    @staticmethod
    def get_summary():
        return VGG16(weights='imagenet', include_top=True).summary()
