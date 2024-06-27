from django.urls import path
from .views.user_views import users

urlpatterns = [
    path('users/', users, name='users'),
    path('users/<int:user_id>/', users, name='user_detail'),
]
