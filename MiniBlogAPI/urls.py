"""
URL configuration for MiniBlogAPI project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


#This file connects your project-level URLs to your app-level URLs 
# and provides a small welcome page at /api/. It is essential for making your API accessible.

#Required so that HTTP requests like /api/posts/ reach your views.py.

from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse


def api_root(request):
    return JsonResponse({
        "message": "Welcome to Mini Blog API",
        "endpoints": [
            "/api/posts/",
            "/api/posts/<id>/",
            "/api/posts/<id>/comments/"
        ]
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api_root),            # <-- Add this
    path('api/', include('blog.urls')),
]