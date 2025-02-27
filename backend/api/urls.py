from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BrandCheckViewSet

router = DefaultRouter()
router.register(r'check-brand', BrandCheckViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('results//', BrandCheckViewSet.as_view({'get': 'retrieve'}), name='brand-check-detail'),
]