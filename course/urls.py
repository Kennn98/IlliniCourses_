from django.urls import path, re_path
from . import views

urlpatterns = [
    # default return search
    path("", views.search, name = "search_page"),
    # course page
    path("courses/<str:subject_number>", views.course, name = "course_page"),
    # ranking page
    path("ranking/", views.ranking, name = "ranking_page"),

    # re_path(r".+", views.error, name = "error_page")
]
