from django.urls import path

from .views import Rootview

urlpatterns = [
    path("", Rootview.as_view(), name="root"),
]
