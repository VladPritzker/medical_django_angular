from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views.user_views import users, upload_avatar, user_detail

urlpatterns = [
    path('users/', users, name='users'),
    path('users/<int:user_id>/', user_detail, name='user_detail'),
    path('users/<int:user_id>/avatar/', upload_avatar, name='upload_avatar'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
