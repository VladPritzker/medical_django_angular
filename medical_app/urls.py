from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.users, name='users'),
    path('users/<int:user_id>/', views.users, name='user_detail'),
]
 
 