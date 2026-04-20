from django.urls import path

from .views import (
    FacilityCreateView,
    FacilityDeleteView,
    FacilityDetailFragmentsView,
    FacilityDetailView,
    FacilityListView,
    FacilityUpdateView,
)

app_name = "facilities"

urlpatterns = [
    path("", FacilityListView.as_view(), name="list"),
    path("new/", FacilityCreateView.as_view(), name="create"),
    path("<int:pk>/", FacilityDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", FacilityUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete/", FacilityDeleteView.as_view(), name="delete"),
    path("<int:pk>/detail-fragments/", FacilityDetailFragmentsView.as_view(), name="detail_fragments"),
]
