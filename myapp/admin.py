from django.contrib import admin
from .models import User

admin.site.site_header = "Library Management System"  
admin.site.site_title = "Library Management System"


# admin.site.register(Download)
admin.site.register(User)

# Register your models here.
