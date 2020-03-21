import re
from models import db, User


def delete_numbers(string):
    result = re.sub('^[\d-]+ ', '#', string)
    return result

def delete_emails(string):
    result = re.sub('([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)', 'CENSURE', string)
    return result

def uname_check(uname):
    return db.query(User).filter(User.username == uname).first()

def email_check(email):
    return db.query(User).filter(User.email == email).first()
