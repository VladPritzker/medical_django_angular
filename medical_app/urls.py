from django.urls import path
from .views.user_views import users
from .views.auth_views import login
from .views.appointment_views import appointments, appointment_detail
from .views.healthhistory_views import health_histories, health_history_detail

urlpatterns = [
    path('users/', users, name='users'),
    path('users/<int:user_id>/', users, name='user_detail'),
    path('login/', login, name='login'),
    path('users/<int:user_id>/appointments/', appointments, name='appointments'),
    path('users/<int:user_id>/appointments/<int:appointment_id>/', appointment_detail, name='appointment_detail'),
    path('users/<int:user_id>/health_histories/', health_histories, name='health_histories'),
    path('users/<int:user_id>/health_histories/<int:health_history_id>/', health_history_detail, name='health_history_detail'),
]
