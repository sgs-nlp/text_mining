from django.urls import path, include
from .routes import document_view

app_name = 'texts_api'

urlpatterns = [
    path('document', document_view),
]
