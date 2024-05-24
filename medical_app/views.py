from django.http import JsonResponse
from .models import CustomUser

def user_list(request):
    users = CustomUser.objects.all().values('username', 'email', 'is_active', 'is_staff', 'is_superuser')
    user_data = list(users)  # Convert the QuerySet to a list of dictionaries
    return JsonResponse(user_data, safe=False)  # Return the data as JSON
