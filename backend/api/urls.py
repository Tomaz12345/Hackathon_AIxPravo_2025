from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BrandCheckViewSet

router = DefaultRouter()
router.register(r'check-brand', BrandCheckViewSet, basename='check-brand')
router.register(r'results', BrandCheckViewSet, basename='results')  # Register results

urlpatterns = [
    path('', include(router.urls)),
]