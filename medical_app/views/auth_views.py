from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate
import json

@csrf_exempt
@require_http_methods(["GET", "POST"])
def login(request):
    if request.method == 'GET':
        return JsonResponse({'message': 'Login endpoint'})

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')

            if not email or not password:
                return HttpResponseBadRequest("Email and password are required fields")

            user = authenticate(request, username=email, password=password)
            if user is not None:
                return JsonResponse({'message': 'Login successful', 'user_id': user.user_id, 'username': user.username})
            else:
                return JsonResponse({'error': 'Invalid credentials'}, status=401)

        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON")
        except Exception as e:
            return HttpResponseBadRequest(f"Error processing request: {str(e)}")

    else:
        return HttpResponseNotAllowed(['GET', 'POST'])
