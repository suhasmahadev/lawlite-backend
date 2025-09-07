from django.urls import path
from .views import DocumentUploadAPIView, DocumentListAPIView, DocumentDetailAPIView

urlpatterns = [
    path('upload/', DocumentUploadAPIView.as_view(), name='document-upload'),
    path('', DocumentListAPIView.as_view(), name='document-list'),
    path('<int:pk>/', DocumentDetailAPIView.as_view(), name='document-detail'),
]
