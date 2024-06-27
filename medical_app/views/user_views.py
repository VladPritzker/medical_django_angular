from django.contrib.auth import authenticate, get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed
import json
import logging

logger = logging.getLogger(__name__)

User = get_user_model()

@csrf_exempt
def users(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            logger.debug(f"Received data: {data}")
            action = data.get('action')
            email = data.get('email')
            password = data.get('password')
            username = data.get('username', None)

            if action not in ['login', 'register']:
                logger.error("Invalid action")
                return HttpResponseBadRequest("Invalid action")

            if action == 'register':
                if not email or not password or not username:
                    logger.error("Username, email, and password are required fields")
                    return HttpResponseBadRequest("Username, email, and password are required fields")
                if User.objects.filter(email=email).exists():
                    logger.error("User with this email already exists")
                    return HttpResponseBadRequest("User with this email already exists")
                user = User.objects.create_user(username=username, email=email, password=password)
                user.is_admin = False  # Set default value for is_admin
                user.save()
                logger.info("Registration successful")
                return JsonResponse({'message': 'Registration successful', 'user_id': user.user_id, 'username': user.username, 'email': user.email}, status=201)

            if action == 'login':
                if not email or not password:
                    logger.error("Email and password are required fields")
                    return HttpResponseBadRequest("Email and password are required fields")
                user = authenticate(request, username=email, password=password)
                if user is not None:
                    logger.info("Login successful")
                    user_data = {
                        'message': 'Login successful',
                        'user_id': user.user_id,
                        'username': user.username,
                        'email': user.email,
                    }
                    return JsonResponse(user_data, status=200)
                else:
                    logger.error("Invalid credentials")
                    return JsonResponse({'error': 'Invalid credentials'}, status=401)

        except json.JSONDecodeError:
            logger.error("Invalid JSON")
            return HttpResponseBadRequest("Invalid JSON")
        except Exception as e:
            logger.exception(f"Error processing request: {str(e)}")
            return HttpResponseBadRequest(f"Error processing request: {str(e)}")

    elif request.method == 'GET':
        try:
            logger.debug("Fetching users")
            users = User.objects.all()
            users_data = [{'user_id': user.user_id, 'username': user.username, 'email': user.email} for user in users]
            logger.debug(f"Users data: {users_data}")
            return JsonResponse(users_data, safe=False)
        except Exception as e:
            logger.exception(f"Error fetching users: {str(e)}")
            return JsonResponse({'error': 'Error fetching users'}, status=500)

    else:
        return HttpResponseNotAllowed(['GET', 'POST'])
