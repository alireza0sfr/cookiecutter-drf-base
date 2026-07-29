"""URL patterns for apps."""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

# from apps.example.views import ExampleViewSet

router = DefaultRouter()
# router.register(r'examples', ExampleViewSet, basename='example')

urlpatterns = [
    path('', include(router.urls)),
    path('base/', include('apps.base.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
]
