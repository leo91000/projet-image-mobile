from django.urls import path
from api.views import ImageView, ImageIdView

urlpatterns = [
    path('img_searches', ImageView.as_view()),
    path('img_searches/<int:img_id>/', ImageIdView.as_view())
];