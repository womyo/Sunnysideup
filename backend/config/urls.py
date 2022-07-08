"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from polls import views
from django.conf.urls import include
from polls.views import RiseSetView, PredictView, RiseView, SetView
from rest_framework import routers, permissions

router = routers.DefaultRouter()

urlpatterns = [
    path(r'', include(router.urls)),
    path('city/<str:post_pk>/date/<int:pk>', RiseSetView.as_view()),
    path('date/<str:pk_1>/lat/<str:pk_2>/lon/<str:pk_3>/standard/<str:pk_4>', PredictView.as_view()),
    path('api/rise/', RiseView.as_view()),
    path('api/set/', SetView.as_view()),
    path('admin/', admin.site.urls),
]
