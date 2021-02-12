from flask import Flask, request,render_template,redirect,flash,session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    """[connect to database]
    """
    db.app = app
    db.init_app(app)


class User(db.Model):
    """User model/class for users table creation and methods for users
    """
    __tablename__ = "users"
    
    @classmethod
    def register(cls,username,password,email,first_name,last_name):
        """register class method for creating a User (registering a new User)
            With a secure and encrypted password that can be stored
        Args:
            username ([type]): [description]
            pwd ([type]): [password]
            email ([type]): [description]
            first_name ([type]): [first_name]
            last_name([type]): [last_name]
        Returns:
            A User object with encrypted password for database storage
        """
        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")
        return cls(username=username,password=hashed_utf8,email=email,first_name=first_name,last_name=last_name)
    
    @classmethod
    def authenticate(cls,username,pwd):
        """validate a an attempted login is allowed and in the database
            and that the password is correct for that user
        Args:
            username ([type]): [description]
            pwd ([type]): [password]
        Returns:
            the user from User query if valid, otherwise false
        """
        user = User.query.filter_by(username=username).first()
        
        if user and bcrypt.check_password_hash(user.password,pwd):
            return user
        else:
            return False
    
    @classmethod
    def reset_password(cls,new_pass,user):
        """ encrypts the new password a user created and stores it as their new password 
        """
        hashed = bcrypt.generate_password_hash(new_pass)
        hashed_utf8 = hashed.decode("utf8")
        user.password = hashed_utf8
        db.session.commit()
    
    @property
    def fullname(self):
        return self.first_name + " " + self.last_name
    
    
    def __repr__(self): 
        """show info about User objects
        """
        u = self
        return f"<User username={u.username}>"
    
    
    username = db.Column(db.String(20),primary_key=True,nullable=False)
    password = db.Column(db.String,nullable=False)
    email = db.Column(db.String(50),unique=True)
    first_name = db.Column(db.String(30),
                     nullable=False,
                     unique=True)
    last_name = db.Column(db.String(30), nullable=False)
    reset_token = db.Column(db.String(500),nullable=True,unique=True)

    feedbacks = db.relationship('Feedback', backref='users',cascade="all, delete")

class Feedback(db.Model):
    """Creates feedbacks table in db and Handles methods for Feedback objects
    """
    __tablename__ = "feedbacks"
     
    def __repr__(self): 
        """show info about Feedback objects
        """
        fb = self
        return f"<Feedback id={fb.id} || title={fb.title} || username={fb.username}>"
    
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String(100),nullable=False)
    content = db.Column(db.String(300),nullable=False)
    username = db.Column(db.String(20),db.ForeignKey('users.username',ondelete="CASCADE"),nullable=False)