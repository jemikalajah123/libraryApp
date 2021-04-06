from django.urls import path
from library.views import book_views as views

urlpatterns = [
    path('', views.getBooks, name="Books"),

    path('create/', views.createBook, name="Book-create"),
    path('upload/', views.uploadImage, name="image-upload"),
    path('borrow/', views.getBorrowedBooks, name="books-borrow"),
    
    path('<str:pk>/', views.getBook, name="Book"),
    path('update/<str:pk>/', views.updateBook, name="Book-update"),
    path('delete/<str:pk>/', views.deleteBook, name="Book-delete"),
]