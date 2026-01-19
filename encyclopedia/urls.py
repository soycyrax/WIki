from django.urls import path

from . import views

urlpatterns = [
    path("wiki/", views.index, name="index"),
    path("wiki/random/", views.random_page, name="random"),
    path("wiki/search/", views.search, name = "search"),
    path("wiki/create/", views.create_new_page, name="create"),
    path("wiki/<str:title>/", views.get_data, name="title"),
    path("wiki/edit/<str:title>/", views.edit, name="edit")
]
