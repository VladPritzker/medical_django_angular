from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from medical_app.models import HealthHistory
import json

@csrf_exempt
@require_http_methods(["GET", "POST"])
def health_histories(request, user_id):
    if request.method == 'GET':
        health_histories = HealthHistory.objects.filter(user_id=user_id).values()
        return JsonResponse(list(health_histories), safe=False)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            health_history = HealthHistory.objects.create(
                user_id=user_id,
                condition=data['condition'],
                treatment=data['treatment'],
                date=data['date']
            )
            return JsonResponse({'health_history_id': health_history.id}, status=201)
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON")
        except Exception as e:
            return HttpResponseBadRequest(f"Error processing request: {str(e)}")

    else:
        return HttpResponseNotAllowed(['GET', 'POST'])

@csrf_exempt
@require_http_methods(["PATCH", "DELETE"])
def health_history_detail(request, user_id, health_history_id):
    try:
        health_history = HealthHistory.objects.get(id=health_history_id, user_id=user_id)
    except HealthHistory.DoesNotExist:
        return JsonResponse({'error': 'Health history not found'}, status=404)

    if request.method == 'PATCH':
        try:
            data = json.loads(request.body)
            if 'condition' in data:
                health_history.condition = data['condition']
            if 'treatment' in data:
                health_history.treatment = data['treatment']
            if 'date' in data:
                health_history.date = data['date']
            health_history.save()
            return JsonResponse({'message': 'Health history updated successfully'})
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON")
        except Exception as e:
            return HttpResponseBadRequest(f"Error processing request: {str(e)}")

    elif request.method == 'DELETE':
        health_history.delete()
        return JsonResponse({'message': 'Health history deleted successfully'})

    else:
        return HttpResponseNotAllowed(['PATCH', 'DELETE'])
