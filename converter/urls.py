# converter/urls.py

from django.urls import path
from .views import ImageViewSet

urlpatterns = [
    # converter 앱 내부의 루트 경로 ('')를 ImageViewSet에 연결
    path('', ImageViewSet.as_view({'post': 'convert_image'}), name='convert'),
]