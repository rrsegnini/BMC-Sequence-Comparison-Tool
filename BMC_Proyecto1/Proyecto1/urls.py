from django.urls import path
from django.views.generic.base import TemplateView
from . import views



urlpatterns = [
    path('', TemplateView.as_view(template_name='main.html')),
    path('', views.search, name='search'),
    path('', views.search2, name='search'),
    path('', views.algorithms, name='algorithms'),
]