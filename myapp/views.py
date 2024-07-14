from django.shortcuts import render
from rest_framework import mixins
from .serializer import *
from rest_framework import viewsets
from .models import User
import json
from .models import *
import datetime
import jwt
from django.conf import settings
from django.http import JsonResponse
from .mixins import JWTAuthMixin
from rest_framework.decorators import action
import django_filters.rest_framework
from rest_framework import filters
from .pagination import CustomPagination
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from django_socketio import events
import json
from .respone_utils import send_response, Status
import requests
from django.shortcuts import get_object_or_404
from .send_mail import send_borrow_email
from .cronjob import scheduler
from .utils import get_book_genre

ISSUE_DAYS = 7
GOOGLE_BOOK_API = "https://www.googleapis.com/books/v1/volumes?q=isbn:"

# Create your views here
class UserDetailView(JWTAuthMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    queryset = User.objects.all()
    context_object_name = 'user'
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend,
                       filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['username', 'email', 'phone']
    search_fields = ['username', 'email', 'phone']
    ordering_fields = ['username', 'email', 'phone']
    lookup_field = 'id'
    serializer_class = UserSerializer
    pagination_class = CustomPagination

    # How to define request content type
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    # Updating request class
    
    @action(detail=False, methods=['put'], url_path='update', url_name='update')      
    def update_user(self, request):  
        if request.method == "PUT":   
            data = request.data
            user = request.user_info
            user.username = data.get('username', user.username)
            user.email = data.get('email', user.email)
            user.phone = data.get('phone', user.phone)
            user.address = data.get('address', user.address)
            user.save()
            return send_response(
                status=Status.OK, 
                data=UserSerializer(user).data, 
                message="User updated successfully"
            )
        return send_response(
            status=Status.BAD_REQUEST, 
            message='Invalid request'
        )

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return send_response(status=Status.CREATED, data=response.data, message='User created successfully1')

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return send_response(status=Status.OK, data=response.data, message='User updated successfully')

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        return send_response(status=Status.OK, data=response.data, message='User deleted successfully')

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return send_response(status=Status.OK, data=response.data, message='User list fetched successfully')

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return send_response(status=Status.OK, data=response.data, message='User fetched successfully')   

    @action(detail=False, methods=['post'], url_path='login', url_name='login')
    def login(self, request):
        if request.method == 'POST':
            data = json.loads(request.body)
            user = User.objects.filter(username=data['username']).first()
            if user and user.check_password(data['password']):
                payload = {
                    'user_id': user.id,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
                    'username': user.username,
                }
                token = jwt.encode(
                    payload, settings.SECRET_KEY, algorithm='HS256')
                return send_response(status=Status.OK, data={
                    'token': token,
                    "user": UserSerializer(user).data
                },
                    message="Token successfully created."
                )
            return send_response(status=Status.BAD_REQUEST, message="Invalid username or password.")
        return send_response(status=Status.BAD_REQUEST, message="Invalid request method")

    

    # @action(detail=False, methods=['post'], url_path='download', url_name='download', parser_classes=[MultiPartParser])
    # def download(self, request):
    #     if request.method == 'POST':
    #         user = request.user_info
    #         download = Download(user=user, raw_file=request.FILES['file'])
    #         download.save()
    #         return send_response(message='File uploaded successfully', data={
    #             'download_url': download.raw_file.url
    #         },
    #         status=Status.OK)
            
    #     return send_response(
    #             status=Status.BAD_REQUEST,  
    #             message="Invalid request"
    #         )

class BookDetailView(JWTAuthMixin, viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = Book.objects.all()
    lookup_field = 'id'
    serializer_class = BookSerializer
    pagination_class = CustomPagination

    # How to define request content type
    parser_classes = [JSONParser, MultiPartParser, FormParser]  
    
    @action(detail=False, methods=['put'], url_path='update', url_name='update')   
    def update_book_issue(self, request):   
        if request.method == "PUT":   
            data = request.data
            book = get_object_or_404(Book, isbn=data['isbn'])   
            book.count += 1   
            book.save()
            book_issue = BookIssue.objects.filter(user=request.user_info, book=book, is_returned=False).first()   
            if book_issue:   
                book_issue.is_returned = True
                book_issue.save()
                return send_response(
                    status=Status.OK, 
                    message="Book returned successfully"
                )
            return send_response(
                status=Status.BAD_REQUEST, 
                message='Book not issued'
            )   
        return send_response(
            status=Status.BAD_REQUEST, 
            message='Invalid request'
        )
    
    @action(detail=False, methods=['get'], url_path='list', url_name='list')   
    def list_books(self, request):   
        username = request.query_params.get('username', '')   
        if username:   
            user = User.objects.filter(username=username).first()
            if user:   
                books = BookIssue.objects.filter(user=user, is_returned=False)  
                serializer = BookIssueSerializer(books, many=True)  
                data = serializer.data
                for ser in data:   
                    ser['isbn']= BookSerializer(Book.objects.get(id=ser['book'])).data['isbn']   
                                
                    
                return send_response(
                    status=Status.OK, 
                    data=data, 
                    message="Books list"
                )
            return send_response(
                status=Status.BAD_REQUEST, 
                message='User not found'
            ) 
    
    @action(detail=False, methods=['post'], url_path='details', url_name='details')  
    def get_book_details(self, request):  
        if request.method == "POST":   
            data = request.data
            book_ids = data['books_isbn']   
            books = Book.objects.filter(isbn__in=book_ids)
            serializer = BookSerializer(books, many=True)
            return send_response(
                status=Status.OK, 
                data=serializer.data, 
                message="Book details"
            )
          
        return send_response(
            status=Status.BAD_REQUEST, 
            message='Invalid request'
            
        )
    
    @action(detail=False, methods=['post'], url_path='issue', url_name='issue')     
    def issue_book(self, request):   
        if request.method == "POST":   
            data = request.data
            user = request.user_info
            book = get_object_or_404(Book, isbn=data['isbn'])                
            if book.count == 0:
                return send_response(
                    status=Status.BAD_REQUEST, 
                    message='Book not available'
                )
            
            return_date = datetime.datetime.now() + datetime.timedelta(days=ISSUE_DAYS)
            book_issue = BookIssue(user=user, book=book, issue_date=datetime.datetime.now(), return_date=return_date)
            book_issue.save()
            book.count -= 1   
            book.save()
            
            book_genre, book_name = get_book_genre(book.isbn)  
            print(book_genre, book_name) 
            if book_genre:   
                for gene in book_genre:  
                    user_genre = UserGenre.objects.filter(user=user, genre=gene).first()   
                    if user_genre:   
                        user_genre.no_time_genere_read += 1
                        user_genre.save()
                    else:   
                        UserGenre(user=user, genre=gene, no_time_genere_read=1).save()
            else:   
                send_response(
                    status=Status.BAD_REQUEST, 
                    message='Book genre not found'
                )   
            
        
            status = send_borrow_email(user.username, user.email, book_name, return_date)                
            
            return send_response(
                status=Status.OK, 
                data={
                    'user': user.username,
                    'isnb': book.isbn,
                    'issue_date': book_issue.issue_date,
                    'return_date': book_issue.return_date
                }, 
                message="Book issued successfully"
            )
          
        return send_response(
            status=Status.BAD_REQUEST, 
            message='Invalid request'    
        )
    
    