from django.urls import path
from api.views import ImageView

urlpatterns = [
    path('images', ImageView.as_view()),
];