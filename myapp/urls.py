from .views import UserDetailView, BookDetailView
from django.urls import path, include
from rest_framework.routers import DefaultRouter
 


router = DefaultRouter()
router.register(r'users', UserDetailView, basename='user')
router.register(r'books', BookDetailView, basename='book')

urlpatterns = [
    path('api/', include(router.urls)),
    
] 
