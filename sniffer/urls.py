from django.urls import path

from . import views

urlpatterns = [
    path("start", views.start_sniffer, name="start"),
    path("stop", views.stop_sniffer, name="stop"),
]