from django.urls import path, include

app_name = 'texts'

urlpatterns = [
    path('api/', include('texts.api.urls')),
]
