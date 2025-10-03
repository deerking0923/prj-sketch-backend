# config/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 이 부분이 정확해야 합니다.
    path('api/converter/', include('converter.urls')), 
]