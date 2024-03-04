from django.core.mail import EmailMessage
import os
import requests
BREVO_TEMPLATE_MAPPING = {}



class Util:
    @staticmethod
    def send_email(data):
        email=EmailMessage(
            subject=data['subject'],
            body=data['body'],
            from_email=os.environ.get('EMAIL_FROM'),
            to=[data['to_email']]
        )
        email.send()


sender= {
    "name": "TopGear",
    "email": os.environ.get('ADMIN_EMAIL_ID')
  }

def brevo_email_send(to, subject='',htmlContent='',textContent=''):
    url = "https://api.brevo.com/v3/smtp/email"
    headers = {
        "Content-Type": "application/json",
        "api-key": os.environ.get('BREVO_API_KEY'),
    }

    data = {
        "to": to,
        "sender":sender,
        "subject": subject,
        "from": os.environ.get('ADMIN_EMAIL_ID'),
        "htmlContent": htmlContent,
        "textContent": textContent,
        "subject": subject
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == [200,201]:
        return response.text
    else:
        print(f"Failed to send email. Status code: {response.status_code}, Response: {response.text}")
        return response.text

