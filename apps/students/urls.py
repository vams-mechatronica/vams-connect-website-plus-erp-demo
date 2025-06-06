from django.urls import path

from .views import (
    DownloadCSVView,
    StudentBulkUploadView,
    StudentCreateView,
    StudentDeleteView,
    StudentDetailView,
    StudentListView,
    StudentUpdateView,
    StudentDashboardView,
    StudentPromotionView
)

urlpatterns = [
    path("list", StudentListView.as_view(), name="student-list"),
    path("<int:pk>/", StudentDetailView.as_view(), name="student-detail"),
    path("dashboard/<int:pk>/", StudentDashboardView.as_view(), name="student-dashboard"),
    path("create/", StudentCreateView.as_view(), name="student-create"),
    path("<int:pk>/update/", StudentUpdateView.as_view(), name="student-update"),
    path("delete/<int:pk>/", StudentDeleteView.as_view(), name="student-delete"),
    path("upload/", StudentBulkUploadView.as_view(), name="student-upload"),
    path("download-csv/", DownloadCSVView.as_view(), name="download-csv"),
    path('promote-students/', StudentPromotionView.as_view(), name='promote-students'),
]
