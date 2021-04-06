from django.urls import path
from library.views import order_views as views
urlpatterns = [

    path('', views.getOrders, name='orders'),
    path('add/', views.addOrderBooks, name='orders-add'),
    path('myorders/', views.getMyOrders, name='myorders'),

    path('borrow-book/<str:pk>/', views.updateBorrowBook, name='borrow-book'),
    path('return-book/<str:pk>/', views.updateReturnBook, name='return-book'),

    path('<str:pk>/', views.getOrderById, name='user-order'),
]