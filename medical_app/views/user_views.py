from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.contrib.auth import authenticate, get_user_model
import json

User = get_user_model()

@csrf_exempt
@require_http_methods(["POST"])
def users(request):
    try:
        data = json.loads(request.body)
        action = data.get('action')
        email = data.get('email')
        password = data.get('password')
        username = data.get('username', None)

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
                    'avatar': user.avatar.url if user.avatar else None,
                }
                return JsonResponse(user_data, status=200)
            else:
                return JsonResponse({'error': 'Invalid credentials'}, status=401)

    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")
    except Exception as e:
        return HttpResponseBadRequest(f"Error processing request: {str(e)}")

@csrf_exempt
@require_http_methods(["POST"])
def upload_avatar(request, user_id):
    try:
        user = get_object_or_404(User, user_id=user_id)
        avatar = request.FILES.get('avatar')
        if not avatar:
            return HttpResponseBadRequest("No avatar uploaded")

        user.avatar.save(avatar.name, ContentFile(avatar.read()), save=True)
        return JsonResponse({'message': 'Avatar uploaded successfully', 'avatar': user.avatar.url}, status=200)
    except Exception as e:
        return JsonResponse({'error': f'Error processing request: {str(e)}'}, status=400)

@csrf_exempt
@require_http_methods(["GET"])
def user_detail(request, user_id):
    try:
        user = get_object_or_404(User, user_id=user_id)
        user_data = {
            'user_id': user.user_id,
            'username': user.username,
            'email': user.email,
            'avatar': user.avatar.url if user.avatar else None,
        }
        return JsonResponse(user_data, status=200)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': f"Error fetching user: {str(e)}"}, status=400)
