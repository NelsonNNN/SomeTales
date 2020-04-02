from app import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    image = db.Column(db.String(20), nullable=False, default='image.jpg')
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    post = db.relationship('Post', backref='author', lazy= True)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image}')"
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    content = db.Column(db.Text, nullable = True)
    date_posted = db.Column(db.Integer, default = datetime.utcnow)
    user_id =db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True) 
    
    def __repr__(self):
        return f"User('{self.title}', '{self.date_posted}')"
