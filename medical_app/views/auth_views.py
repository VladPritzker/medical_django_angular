from django.contrib.auth import authenticate, get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.views.decorators.http import require_http_methods
import json

User = get_user_model()

@csrf_exempt
@require_http_methods(["POST"])
def users(request):
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

    return HttpResponseNotAllowed(['POST'])
