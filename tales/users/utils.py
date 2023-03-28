import os
import secrets
from PIL import Image
from flask import url_for, current_app
from tales import mail
from flask_mail import Message

def save_image(form_image):
    hex_image=secrets.token_hex(8)
    _, file_ext = os.path.splitext(form_image.filename)
    changed_img = hex_image+ file_ext
    img_path = os.path.join(current_app.root_path, 'static/profilepic', changed_img)
    
    output_size=(125, 125)
    i=Image.open(form_image)
    i.thumbnail(output_size)
    i.save(img_path)
    return changed_img

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Request to reset password', sender = 'nelsonic2550@gmail.com', recipients=[user.email])
    msg.body = f''' A request has been made to change your password. Visit this link to 
reset your password: {url_for('users.reset_token', token=token, _external=True)}
Please ignore this message if you did not make this request.
'''
    mail.send(msg)