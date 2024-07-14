import time
from .send_mail import send_reminder    
from .models import BookIssue, Book, User  
import datetime
from django.utils import timezone
from datetime import timedelta
from .utils import get_book_genre
from apscheduler.schedulers.background import BackgroundScheduler



threshold_time = timezone.now() - timedelta(days=7)  # Adjust the hours as needed

def send_remainder_email():   
    print("Running the cron job")
    users = User.objects.all()  
    for user in users:   
        book_issues = BookIssue.objects.filter(user=user, is_returned=False)    
        for book_issue in book_issues:   
            if (book_issue.return_date >  threshold_time) or (book_issue.return_date - threshold_time < timedelta(hours=6)):   
                book = Book.objects.get(id=book_issue.book_id)

                book_name = get_book_genre(book.isbn)[-1]
                send_reminder(user.username,user.email, book_name, book_issue.return_date)   
     
                print("Email sent to", user.email)   
                
                
scheduler = BackgroundScheduler()
scheduler.add_job(send_remainder_email, 'interval', hours=1)  # Adjust interval as needed
