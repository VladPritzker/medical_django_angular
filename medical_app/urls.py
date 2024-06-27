from django.urls import path
from .views.user_views import users

urlpatterns = [
    path('users/', users, name='users'),
]
