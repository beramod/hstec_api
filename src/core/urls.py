from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from .views import TemplateView

urlpatterns = [
    url(r'^$', TemplateView.as_view(), name='template'),
    url(r'^', TemplateView.as_view(), name='template')
]