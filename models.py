from flask_sqlalchemy import SQLAlchemy
import datetime
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), nullable=False, unique = True)
    first_name = db.Column(db.String(200))
    last_name = db.Column(db.String(200))
    post = db.relationship("Post")
    comment = db.relationship("Comment", backref="user")
    
    def serialize(self):
        return{
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name
        }

class Post(db.Model):
    __tablename__ = "post"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    subtitle = db.Column(db.String(300))
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    comment = db.relationship("Comment")

    def serialize(self):
        return{
            "id": self.id,
            "title": self.title,
            "subtitle": self.subtitle,
            "body": self.body,
            "created_at": self.created_at,
            "user_id": self.user_id
        }

class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False) 
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())  
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))

    def serialize(self):
        return{
            "id": self.id,
            "text": self.text,
            "created_at": self.created_at,
            "user_id": self.user_id,
            "name": self.user.first_name+ " " + self.user.last_name,#agregado para consultar un dato relacinado de otra tabla
            "post_id": self.post_id
        }