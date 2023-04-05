from django.urls import path, include


urlpatterns = [
    path('data_pipeline/', include('data_pipeline.urls')),
]
