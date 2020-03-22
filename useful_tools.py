import re
from app.models import db, User
import smtplib
import ssl
import json

class PersonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, User):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)


def delete_numbers(string):
    result = re.sub('^[\d-]+ ', '#', string)
    return result

def delete_emails(string):
    result = re.sub('([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)', 'CENSURE', string)
    return result

def uname_check(uname):
    return db.session.query(User).filter(User.username == uname).first()

def email_check(email):
    return db.session.query(User).filter(User.email == email).first()

def send_mail(email, description='День рождения сына!'):
    sender_email = "notificationssender.eHack@gmail.com"
    password = "##CENSURED##"
    port = 465  # For SSL
    # Create a secure SSL context
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        message = '''Subject: Вас выбрали для меропртиятия!\n\nДоброго времени суток, Вы были выбраны для меропртиятия. Вот его описание:
{}
        '''.format(description)
        message = message.encode('utf-8')
        server.login(sender_email, password)
        server.sendmail(sender_email, email, message)
