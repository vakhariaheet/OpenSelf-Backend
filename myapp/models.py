from django.db import models
from django.db.models.base import Model
from .fields import EncryptionField
from cloudinary_storage.storage import RawMediaCloudinaryStorage
from enum  import Enum

class Role:  
    USER = 'user'  
    LIBRARIAN = 'librarian'   
    CHOICES = (  
        (USER, 'user'),
        (LIBRARIAN, 'librarian'),
    )
    
class User(models.Model):   
    username = models.CharField(max_length=100, unique=True, null=False)   
    password = EncryptionField(max_length=100)   
    email = models.EmailField()  
    phone = models.CharField(max_length=20)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    address = models.TextField(default="")
    role = models.CharField(max_length=20, choices=Role.CHOICES, default=Role.USER)

    def __str__(self):
        return self.username   

    def check_password(self, password):
        return self.password == password
    
    class Meta:
        db_table = "user"

class Book(models.Model):    
    isbn = models.CharField(max_length=100, unique=True)
    count = models.IntegerField(null=True)
    arriving_date = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)    
    updated_at = models.DateTimeField(auto_now=True)    
    
    class Meta:        
        db_table = "book"
            
    def __str__(self):        
        return self.isbn

class UserGenre(models.Model):   
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    genre = models.CharField(max_length=100)
    no_time_genere_read = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)   
    updated_at = models.DateTimeField(auto_now=True)   
    
    def __str__(self):        
        return self.user.username + " " + self.genre    
    
    class Meta:  
        db_table = "user_genre"
    
class BookIssue(models.Model):   
    user = models.ForeignKey(User, on_delete=models.CASCADE)   
    book = models.ForeignKey(Book, on_delete=models.CASCADE)   
    issue_date = models.DateTimeField()
    return_date = models.DateTimeField()   
    is_returned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)   
    updated_at = models.DateTimeField(auto_now=True)   
    
    class Meta:        
        db_table = "book_issue"    
    
    def __str__(self):        
        return self.user.username + " " + self.book.isbn


# class Download(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     raw_file = models.ImageField(upload_to='raw/', blank=True, storage=RawMediaCloudinaryStorage())
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         db_table = "download"

#     def __str__(self):
#         return self.user.username + " " + self.raw_file.url


# class ChatMessage(models.Model):
#     sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
#     receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
#     # chat = models.ForeignKey('Chat', on_delete=models.CASCADE)
#     text = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         db_table = "chat_message"

#     def __str__(self):
#         return self.sender.username + " " + self.text

# class Chat(models.Model):
#     short_id = models.CharField(max_length=10, unique=True)
#     users = models.ManyToManyField(User, related_name='chats')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         db_table = "chat"

#     def __str__(self):
#         return self.short_id