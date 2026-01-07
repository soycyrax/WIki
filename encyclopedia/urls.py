from django.urls import path

from . import views

urlpatterns = [
    path("wiki/", views.index, name="index"),
    path("wiki/search/", views.search, name = "search"),
    path("wiki/create/", views.create_new_page, name="create"),
    path("wiki/<str:title>/", views.get_data, name="title")
]
