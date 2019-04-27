"""BMC_Proyecto1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import include, path
from Proyecto1 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main/', include('Proyecto1.urls')),
    path('search/', views.search),
    path('search/', views.search2),
    path('main/algorithms/', views.algorithms),
    path('algorithms/', views.algorithms),
    path('exe_algorithms/', views.exe_algorithms),
]
