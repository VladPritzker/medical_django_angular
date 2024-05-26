from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import CustomUser
import json

@csrf_exempt
@require_http_methods(["GET", "POST", "DELETE"])
def users(request, user_id=None):
    if request.method == 'GET':
        users = CustomUser.objects.all().values('id', 'username', 'email', 'is_active', 'is_staff', 'is_superuser')
        user_data = list(users)
        return JsonResponse(user_data, safe=False)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')

            if not username or not email or not password:
                return HttpResponseBadRequest("Username, email, and password are required fields")

            user = CustomUser.objects.create_user(username=username, email=email, password=password)
            return JsonResponse({'id': user.id, 'username': user.username, 'email': user.email}, status=201)
        except Exception as e:
            return HttpResponseBadRequest(str(e))

    elif request.method == 'DELETE':
        if not user_id:
            return HttpResponseBadRequest("User ID is required")

        try:
            user = CustomUser.objects.get(id=user_id)
            user.delete()
            return JsonResponse({'message': 'User deleted successfully'}, status=200)
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except Exception as e:
            return HttpResponseBadRequest(str(e))

    else:
        return HttpResponseNotAllowed(['GET', 'POST', 'DELETE'])
