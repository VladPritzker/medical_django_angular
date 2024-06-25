from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from medical_app.models import Appointment
import json

@csrf_exempt
@require_http_methods(["GET", "POST"])
def appointments(request, user_id):
    if request.method == 'GET':
        appointments = Appointment.objects.filter(user_id=user_id).values()
        return JsonResponse(list(appointments), safe=False)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            appointment = Appointment.objects.create(
                user_id=user_id,
                doctor=data['doctor'],
                appointment_date=data['appointment_date'],
                notes=data.get('notes', '')
            )
            return JsonResponse({'appointment_id': appointment.id}, status=201)
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON")
        except Exception as e:
            return HttpResponseBadRequest(f"Error processing request: {str(e)}")

    else:
        return HttpResponseNotAllowed(['GET', 'POST'])

@csrf_exempt
@require_http_methods(["PATCH", "DELETE"])
def appointment_detail(request, user_id, appointment_id):
    try:
        appointment = Appointment.objects.get(id=appointment_id, user_id=user_id)
    except Appointment.DoesNotExist:
        return JsonResponse({'error': 'Appointment not found'}, status=404)

    if request.method == 'PATCH':
        try:
            data = json.loads(request.body)
            if 'doctor' in data:
                appointment.doctor = data['doctor']
            if 'appointment_date' in data:
                appointment.appointment_date = data['appointment_date']
            if 'notes' in data:
                appointment.notes = data['notes']
            appointment.save()
            return JsonResponse({'message': 'Appointment updated successfully'})
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON")
        except Exception as e:
            return HttpResponseBadRequest(f"Error processing request: {str(e)}")

    elif request.method == 'DELETE':
        appointment.delete()
        return JsonResponse({'message': 'Appointment deleted successfully'})

    else:
        return HttpResponseNotAllowed(['PATCH', 'DELETE'])
