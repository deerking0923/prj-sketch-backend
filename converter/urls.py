# converter/urls.py
from django.urls import path
from .views import ImageViewSet

urlpatterns = [
    path('', ImageViewSet.as_view({'post': 'convert_image'}), name='convert'),
    path('styles/', ImageViewSet.as_view({'get': 'styles'}), name='styles'),
]