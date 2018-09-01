"""bankco2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework import routers
from django.urls import path, include

from bankco2.views import StepViewSet
from . import views

router = routers.DefaultRouter()
router.register(r'steps', StepViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('accounts/', include('allauth.urls')),
    path('animal/', views.AnimalView.as_view(), name='animal'),
    path('drawing/<str:device_id>/', views.draw, name='drawing'),
    path('history/', views.HistoryView.as_view(), name='history'),
    path('rank/', views.RankView.as_view(), name='rank'),
    path('main/', views.MobileMainView.as_view(), name='main'),
    path('', views.IndexView.as_view(), name='index')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
