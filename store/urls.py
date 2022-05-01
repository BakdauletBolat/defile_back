from django.urls import path
from .views import (AddProductToBasket,GetOrderToUser,
                    CreateOrderUnauthorizedUser,CreateOrderAuthorizedUser,
                    OrderListApiView,OrderQtyUpdateView)
urlpatterns = [
    path('add-to-basket/', AddProductToBasket.as_view()),
    path('get-order/',GetOrderToUser.as_view()),
    path('get-orders/',OrderListApiView.as_view()),
    path('create-unauthorized-order/',CreateOrderUnauthorizedUser.as_view()),
    path('create-authorized-order/',CreateOrderAuthorizedUser.as_view()),
    path('update-order-qty/',OrderQtyUpdateView.as_view())
]