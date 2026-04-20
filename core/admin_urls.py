from django.urls import path

from .views import AdminAccessDeleteView, AdminAccessEditView, AdminDashboardView

app_name = "core_admin"

urlpatterns = [
    path("", AdminDashboardView.as_view(), name="dashboard"),
    path("access/<int:pk>/edit/", AdminAccessEditView.as_view(), name="edit_access"),
    path("access/<int:pk>/delete/", AdminAccessDeleteView.as_view(), name="delete_access"),
]
