from django.urls import path

from . import views

urlpatterns = [
    path("wiki/", views.index, name="index"),
    path("wiki/<str:title>/", views.get_data, name="title"),
    path("wiki/search/", views.search, name = "search")
]
