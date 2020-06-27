import os

class Config:
    SECRET_KEY= os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI='postgres://uxsmwuxgkvknfl:f4070b9fb7a07173c8635b42f1f9c4e30f234dd172b605985054c4d60db493d3@ec2-52-204-232-46.compute-1.amazonaws.com:5432/d20e4i66qantoc' 
    MAIL_SERVER='smtp.googlemail.com'
    MAIL_PORT=587
    MAIL_USE_TLS = True
    MAIL_USERNAME= os.environ.get('EMAIL_USER')
    MAIL_PASSWORD= os.environ.get('EMAIL_PASS')