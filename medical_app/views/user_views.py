from django.contrib.auth import get_user_model, authenticate
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.views.decorators.http import require_http_methods
import json

User = get_user_model()

@csrf_exempt
@require_http_methods(["GET", "POST"])
def users(request, user_id=None):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            action = data.get('action')
            email = data.get('email')
            password = data.get('password')
            username = data.get('username', None)

            if action not in ['login', 'register']:
                return HttpResponseBadRequest("Invalid action")

            if action == 'register':
                if not email or not password or not username:
                    return HttpResponseBadRequest("Username, email, and password are required fields")
                if User.objects.filter(email=email).exists():
                    return HttpResponseBadRequest("User with this email already exists")
                user = User.objects.create_user(username=username, email=email, password=password)
                return JsonResponse({'message': 'Registration successful', 'user_id': user.user_id, 'username': user.username, 'email': user.email}, status=201)

            if action == 'login':
                if not email or not password:
                    return HttpResponseBadRequest("Email and password are required fields")
                user = authenticate(request, username=email, password=password)
                if user is not None:
                    user_data = {
                        'message': 'Login successful',
                        'user_id': user.user_id,
                        'username': user.username,
                        'email': user.email,
                    }
                    return JsonResponse(user_data, status=200)
                else:
                    return JsonResponse({'error': 'Invalid credentials'}, status=401)

        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON")
        except Exception as e:
            return HttpResponseBadRequest(f"Error processing request: {str(e)}")
    
    elif request.method == 'GET':
        if user_id:
            try:
                user = User.objects.get(user_id=user_id)
                user_data = {
                    'user_id': user.user_id,
                    'username': user.username,
                    'email': user.email,
                    'is_active': user.is_active,
                    'is_staff': user.is_staff,
                    'is_admin': user.is_admin,
                }
                return JsonResponse(user_data, status=200)
            except User.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)
        else:
            users = User.objects.all()
            users_data = [{'user_id': user.user_id, 'username': user.username, 'email': user.email} for user in users]
            return JsonResponse(users_data, safe=False)

    else:
        return HttpResponseNotAllowed(['GET', 'POST'])
