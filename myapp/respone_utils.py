from django.http import JsonResponse
from rest_framework import status as http_status

class Status:
    OK = 200
    CREATED = 201
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    CONFLICT = 409
    INTERNAL_SERVER_ERROR = 500

def create_response(status, data=None, message=None):
    response = {
        'isSuccess': status in {Status.OK, Status.CREATED},
        'message': message or get_default_message(status),
        'data': data
    }
    return response

def get_default_message(status):
    messages = {
        Status.OK: 'Action Successful',
        Status.CREATED: 'Created Successfully',
        Status.BAD_REQUEST: 'Bad Request',
        Status.UNAUTHORIZED: 'Authentication Failed',
        Status.FORBIDDEN: 'Forbidden',
        Status.NOT_FOUND: 'Not Found',
        Status.CONFLICT: 'Conflict',
        Status.INTERNAL_SERVER_ERROR: 'Internal Server Error'
    }
    return messages.get(status, '')

def send_response(status, data=None, message=None):
    response_data = create_response(status, data, message)
    return JsonResponse(response_data, status=status)
