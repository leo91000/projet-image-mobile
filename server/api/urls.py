from django.urls import path
from api.views import ImageView, ImageIdView, IndexerView, ImageFileView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('img_searches', ImageView.as_view()),
    path('img_searches/<int:img_id>/', ImageIdView.as_view()),
    path('images/<int:img_id>/<str:img_name>', ImageFileView.as_view()),
    path('index', IndexerView.as_view())
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
