from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>", views.title, name="pages"),
    path("search", views.search, name="search"),
    path("new", views.new, name="new"),
    path("edit/<str:name>/", views.edit, name="edit-page"),
    path("random", views.randomPage, name="random")
]
