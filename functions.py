from flask import Flask, request,render_template,redirect,flash,session,flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from models import db, connect_db,User,Feedback



def delete_user(token):
    """ Function that handles deleting a user based on token authorization
    """
    Feedback.query.filter(Feedback.username == token).delete()
    db.session.commit()
    User.query.filter_by(username=token).delete()    
    db.session.commit()
    session.pop("username")
    return True

def delete_feedback(token):
    """ Function that handles deleting a feedback based on token authorization
    """
    Feedback.query.filter_by(id=token).delete()
    db.session.commit()
    return True

def check_session_status(username):
    """Function that checks the status of a user.
        1.) Is there is username in session?
        2.) Is the username in session equal to the username of an attempted account access?
            (i.e. Is user1 trying to access user2 wrongfully)
        3.) Return a redirect path based on the user's level of autherization
    """
    if "username" in session and session["username"] == username:
        return "authorized"
    elif "username" in session and session["username"] != username:
        return ["not_authorized",f"/users/{session['username']}"]
    else:
        return ["not_logged","/login"]

def common_flashes(flash):
    """Dictionary of common flashes to be re-used
        currently in dictionary:
        1.) "not_logged" - for a flash message if there is no logged in user
        2.) "not_authorized" - for a flash message if the user is not authorized
        3.) "fb_deleted" - for a flash message stating that the feedback has been deleted
        4.) "missing_user" - flash for if user not in the database 
        5.) "password_reset" - flash for successful password reset
    """
    flashes = {
        "not_logged":["You are not logged in. Please login or signup and try again",'alert-danger'],
        "not_authorized":["You Are Not Authorized To View That Account",'alert-danger'],
        "fb_deleted":["Feedback Has Been Deleted","alert-success"],
        "missing_user": ["Account Not In The System, Please Create An Account","alert-warning"],
        "password_reset": ["Your Password Has Successfully Been Reset, Try Logging In Again","alert-success"]
    }
    message = flashes[flash] 
    return message

def verify_email(email):
    """ function used for verifying users email is in the database system
    """
    user = User.query.filter_by(email=email).first()
    if user:
        return user
    else:
        return False

def verify_token(token):
    """ function for verifying the token in a query string
        for password reset
    """
    user = User.query.filter_by(reset_token=token).first()
    if user:
        return user
    else:
        return False