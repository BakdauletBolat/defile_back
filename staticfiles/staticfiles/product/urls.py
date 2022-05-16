from django.urls import path
from .views import (ProductListApiView,BrandListApiView,TypeListApiView,
                    CategoryListApiView,ProductRetrieveAPIView,AddToFavorites,
                    ProductFavoritesListAPIView)

urlpatterns = [
    path('',ProductListApiView.as_view()),
    path('<int:pk>/',ProductRetrieveAPIView.as_view()),
    path('like/',AddToFavorites.as_view()),
    path('favorites/',ProductFavoritesListAPIView.as_view()),
    path('brand/',BrandListApiView.as_view()),
    path('type/',TypeListApiView.as_view()),
    path('category/',CategoryListApiView.as_view()),
]