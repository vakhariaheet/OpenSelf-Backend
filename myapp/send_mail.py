import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import json
import requests
from dotenv import load_dotenv
load_dotenv()

# Set your SendGrid API key


api_key = os.getenv("api_key")


def send_new_arrivals_message():
    return requests.post(
       	"https://api.mailgun.net/v3/odoo.heetvakharia.in/messages",
        auth=("api", api_key),
        data={"from": "Mailgun Sandbox <postmaster@odoo.heetvakharia.in>",
              "to": "Heet Vakharia <support@webbound.in>",
              "subject": "Hello Kathan Vakharia",
              "template": "new-arrivals",
                          "h:X-Mailgun-Variables": '{"test": "test"}',
              "t:variables": json.dumps({
                  "title_image": "https://logos-world.net/wp-content/uploads/2020/09/Google-Logo-700x394.png",
                  "newarrivals_title": "Hey Heet",
                  "newarrivals_body": "Check out our latest arrivals!",
                  "newarrivals_book1": "The Great Gatsby",
                  "newarrivals_book2": "The Bell Jar",
                  "newarrivals_book3": "I Know Why the Caged Bird Sings",
              })
              })

def send_borrow_email(username, email, name, due_date):
    
    try:
    
        resp = requests.post(
                "https://api.mailgun.net/v3/odoo.heetvakharia.in/messages",
                    auth=("api", api_key),
                    data={"from": "Mailgun Sandbox <postmaster@odoo.heetvakharia.in>",
                                "to": f"{username} <{email}>",
                                "subject": "Book Issue Successful!",
                                "template": "due-date",
                                "h:X-Mailgun-Variables": '{"test": "test"}',
                        "t:variables": json.dumps({
                            "username": username,
                            "body": f'Hi {username},Your book has been successfully issued! \n Due Date: {due_date.strftime("%d-%m-%y")}',
                        })},

                                )

        print(resp.status_code)
        if resp.status_code == 200:
            return True
        else:
            return False
    except Exception as e:
        return False


def send_reminder(username, email, book, return_date):
    try:
        resp = requests.post(
                "https://api.mailgun.net/v3/odoo.heetvakharia.in/messages",
                    auth=("api", api_key),
                    data={"from": "Mailgun Sandbox <postmaster@odoo.heetvakharia.in>",
                                "to": f"{username} <{email}>",
                                "subject": "Reminder: Upcoming Due Date",
                                "template": "reminder",
                                "t:variables": json.dumps({
                                    "username": username,
                                    "book": f'{book.upper()} on {return_date.strftime("%d-%m-%y")}',
                                })
                        
                                })
    
        print(resp.status_code)
        if resp.status_code == 200:
            return True
        else:
            return False
    except Exception as e:
        return False
