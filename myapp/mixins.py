# yourapp/mixins.py

from django.http import JsonResponse
import jwt
from django.conf import settings
from .models import User
import json
import datetime
from .serializer import UserSerializer
from .respone_utils import Status, send_response


class JWTAuthMixin:
    def dispatch(self, request, *args, **kwargs):
        url = request.build_absolute_uri()

        if url.endswith("books/details/") and request.method == 'POST':
            return super().dispatch(request, *args, **kwargs)   
        
        if "/books" in url and request.method in ['GET']:
                    return super().dispatch(request, *args, **kwargs)
        
        token = request.META.get('HTTP_AUTHORIZATION', '').split('Bearer ')[-1]

        if url.endswith("login/") and request.method == 'POST':
            return super().dispatch(request, *args, **kwargs)
        
        if url.endswith("detail/") and request.method == 'GET':   
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                user = User.objects.get(id=payload['user_id'])
                request.user_info = user
                return send_response(status=Status.OK, data=UserSerializer(user).data, message='User fetched successfully')
            except (jwt.ExpiredSignatureError, jwt.DecodeError, User.DoesNotExist):
                return send_response(status=Status.UNAUTHORIZED, message="Invalid token or user not found")
            
        if url.endswith("users/") and request.method == 'POST':
            
            serializer = UserSerializer(data=json.loads(request.body))
            if serializer.is_valid():
                user = serializer.save()

                payload = {
                    'user_id': user.id,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1), 
                    'username': user.username,
                    'email': user.email,
                    'role': user.role,
                    'phone': user.phone,
                    'address': user.address
                }

                token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
                return send_response(status=Status.CREATED, data = {
                    'token':token,
                      "user": serializer.data
                },
                message='User created successfully'
                )
        
        if token:
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                user = User.objects.get(id=payload['user_id'])
                request.user_info = user
                
            except (jwt.ExpiredSignatureError, jwt.DecodeError, User.DoesNotExist):
                return send_response(status=Status.UNAUTHORIZED, message="Invalid token or user not found")
        else:
            return send_response(status=Status.UNAUTHORIZED, message="Authentication credentials were not provided." )
           
        return super().dispatch(request, *args, **kwargs)
