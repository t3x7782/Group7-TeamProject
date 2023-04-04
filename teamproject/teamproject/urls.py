"""teamproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from geektext import views
from geektext.views import book_comments



urlpatterns = [
    path('admin/', admin.site.urls),
    #path('books/', include('books.urls')),
    path('books/', views.create_book),
    path('books/<str:isbn>/', views.retrieve_book),
    path('authors/', views.create_author),
    path('authors/<int:author_id>/books/', views.list_books_by_author),
    
    #priscilla's urls
    path('book/<int:pk>/', views.book_individual.as_view()),
    path('books/<int:book_id>/comments/', book_comments, name='book_comments'),
    path('comments/', views.comment_list.as_view()),
    path('comment/<int:pk>/', views.comment_individual.as_view()),
    path('ratings/', views.rating_list.as_view()),
    path('rating/<int:pk>/', views.rating_individual.as_view()),
    #path('books/<int:book_id>/avg_rating/', book_average_rating, name='book_average_rating')
    #path('books/<int:book_id>/avg_rating/', views.book_rating_average, name='book_average_rating')

    path('admin/', admin.site.urls),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserIndividual.as_view()),
    path('creditcard/', views.CreditCardList.as_view()),
    path('creditcard/<int:pk>/', views.CreditCardIndividual.as_view()),
    path('users/create/', views.CreateUserView.as_view(), name='create_user'),
    path('users/<username>/', views.GetUserView.as_view()),
    path('api/users/<str:username>/', views.UserUpdate.as_view()),
    path('api/users/create_credit_card', views.CreditCardCreate.as_view()),
]
