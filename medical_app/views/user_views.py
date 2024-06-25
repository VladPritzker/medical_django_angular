from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate
from medical_app.models import CustomUser
import json
@csrf_exempt
@require_http_methods(["GET", "POST", "DELETE"])
def users(request, user_id=None):
    if request.method == 'GET':
        if user_id:
            try:
                user = CustomUser.objects.get(user_id=user_id)
                user_data = {
                    'user_id': user.user_id,
                    'username': user.username,
                    'email': user.email,
                    'is_active': user.is_active,
                    'is_staff': user.is_staff
                }
                return JsonResponse(user_data, safe=False)
            except CustomUser.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)
        else:
            users = CustomUser.objects.all().values('user_id', 'username', 'email', 'is_active', 'is_staff')
            user_data = list(users)
            return JsonResponse(user_data, safe=False)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("Received data:", data)  # Print the received data for debugging
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')

            if not username or not email or not password:
                return HttpResponseBadRequest("Username, email, and password are required fields")

            # Check if email already exists
            if CustomUser.objects.filter(email=email).exists():
                return HttpResponseBadRequest("Email already exists")

            user = CustomUser.objects.create_user(username=username, email=email, password=password)
            return JsonResponse({'user_id': user.user_id, 'username': user.username, 'email': user.email}, status=201)

        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON")
        except Exception as e:
            return HttpResponseBadRequest(f"Error processing request: {str(e)}")

    elif request.method == 'DELETE':
        if not user_id:
            return HttpResponseBadRequest("User ID is required")

        try:
            user = CustomUser.objects.get(user_id=user_id)
            user.delete()
            return JsonResponse({'message': 'User deleted successfully'}, status=200)
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except Exception as e:
            return HttpResponseBadRequest(f"Error processing request: {str(e)}")

    else:
        return HttpResponseNotAllowed(['GET', 'POST', 'DELETE'])
