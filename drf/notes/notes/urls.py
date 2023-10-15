"""
URL configuration for notes project.
"""
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularJSONAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework import routers

from notes.views import NoteViewSet

router = routers.DefaultRouter()
router.register("notes", NoteViewSet)

urlpatterns = [
    path("", include(router.urls)),
    # spectacular doc:
    path("openapi.json", SpectacularJSONAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view()),
    path("redoc/", SpectacularRedocView.as_view()),
]
