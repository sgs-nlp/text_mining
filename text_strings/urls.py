from django.urls import path, include

app_name = 'text_srtring'

urlpatterns = [
    path('api/', include('text_strings.api.urls')),
]
