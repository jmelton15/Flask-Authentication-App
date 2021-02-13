# from config import secret_keys
import os
from flask import Flask, request,render_template,redirect,flash,session,flash
from flask_mail import Mail, Message
import secrets
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc
from models import db, connect_db,User,Feedback
from forms import LoginForm,SignUpForm,FeedbackForm,EmailConfirmationForm, PasswordResetForm
from flask_bcrypt import Bcrypt
from functions import check_session_status,common_flashes,delete_feedback,delete_user,verify_email,verify_token

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','postgresql:///authenticate')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY',"SUPERSECRETKEY")

app.config['MAIL_SERVER'] = os.environ.get('MAIL_USERNAME','smtp.gmail.com')
app.config['MAIL_PORT'] = os.environ.get('MAIL_PORT',587)
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', True)
app.config['MAIL_USE_SSL'] = os.environ.get('MAIL_USE_SSL', False)
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_SUPPRESS_SEND'] = os.environ.get('MAIL_SUPPRESS_SEND')
app.config['TESTING'] = False


mail = Mail(app)

connect_db(app)
# db.create_all()



@app.route('/')
def register_redirect():
    """HomePage Redirects to the register page
    """
    return redirect("/register")

@app.route("/password/forgot",methods=["GET","POST"])
def send_password_reset():
    """ Handle showing the email authenticate page and sending password reset code
     I got everything to setup the mail server from the Flask Mail documents
     and then got the token creation from secrete module documentation on python
    """
    form = EmailConfirmationForm()
    if form.validate_on_submit():
        email = form.email.data
        user = verify_email(email)
        if user:
            token = secrets.token_urlsafe(32)
            url = os.environ.get('URL') + token
            body = f"""Hello, This Is The Password Reset Code You Asked For. 
                Type this into the confirmation box on the page to verify and reset your password\n 
                {url}"""
            subject = "Password Reset Confirmation Code" 
            msg = Message(recipients=[email],body=body,subject=subject)
            mail.send(msg)
            user.reset_token = token # store the token temporarily so we can verfiy the user
            db.session.commit()
            flash("Code Has Been Sent and Should Be In Your Email Shortly","alert-success")
            return redirect("/password/forgot")
        else:
            message = common_flashes("missing_user")
            flash(message[0],message[1])
            return redirect("/login")
    return render_template("email_form.html",form=form)

@app.route("/password",methods=["GET","POST"])
def verify_and_show_reset():
    token = request.args.get('reset')
    user = verify_token(token)
    if user:
        form = PasswordResetForm()
        if form.validate_on_submit():
            new_pass = form.password.data
            User.reset_password(new_pass,user)
            message = common_flashes("password_reset")
            flash(message[0],message[1])
            user.reset_token = None # we want to erase the token from the database once this is done
            db.session.commit()
            return redirect("/login")
        return render_template("password_reset_page.html",form=form)
    
@app.route('/logout') 
def logout_user():
    """handles logging out a user and redirects to login page/homepage
    """
    session.pop("username")
    return redirect('/login')

@app.route("/register",methods=["GET","POST"])
def show_register_page():
    """Shows register page with signup form
    """
    signup_form = SignUpForm() 
    if signup_form.validate_on_submit():
        user_data = {k:v for k,v in signup_form.data.items() if k != "csrf_token" and k != 'confirm_pass'}
        print(user_data)
        new_user = User.register(**user_data)
        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            signup_form.username.errors.append("Username Is Taken. Please Pick Another")
        session["username"] = new_user.username
        flash(f"Thanks For Signing up, {new_user.username}!","alert-success")
        return redirect(f"/users/{new_user.username}")
    return render_template("register.html",form=signup_form)
        
@app.route("/login",methods=["GET","POST"])
def show_login_page():
    """Shows login page and login form
    """
    login_form = LoginForm()
    if login_form.validate_on_submit():
        username = login_form.username.data
        pwd = login_form.password.data
            
        user = User.authenticate(username,pwd)
        if user:
            session["username"] = user.username
            flash(f"Welcome back, {user.username}!","alert-primary")
            return redirect(f"/users/{user.username}")
        else:
            login_form.username.errors = ["Incorrect Username or Password. Please Try Again"]
    return render_template("login.html",form=login_form)
    
@app.route("/users/<username>",methods=["GET","POST"])
def show_account_page(username):
    """Shows the account page of a given user when and if the user is logged in
    """
    if check_session_status(username) != "authorized":
        message = common_flashes(check_session_status(username)[0])
        flash(message[0],message[1])
        return redirect(check_session_status(username)[1])
    else:
        user = User.query.filter_by(username=username).first()
        return render_template("user_account.html",user=user)

@app.route("/users/<username>/delete",methods=["POST"])
def delete_user(username):
    """Handles deleting a user from the web app and database
    """
    if check_session_status(username) != "authorized":
        message = common_flashes(check_session_status(username)[0])
        flash(message[0],message[1])
        return redirect(check_session_status(username)[1])
    if delete_user(username):
        flash("Sorry To See You Leave, We Welcome You Back Anytime!", "alert-warning")
        return redirect("/register")
    else:
        return redirect(f"/users/{session['username']}")

@app.route("/users/<username>/feedback/delete",methods=["POST"])
def delete_users_feedback(username):
    """ Handles deleting a single feedback object from a user
    """
    if check_session_status(username) != "authorized":
        message = common_flashes(check_session_status(username)[0])
        flash(message[0],message[1])
        return redirect(check_session_status(username)[1])
    fb_id = request.form["del-fb-btn"]
    if delete_feedback(fb_id):
        message = common_flashes("fb_deleted")
        flash(message[0],message[1])
    return redirect(f"/users/{session['username']}")

@app.route("/users/<username>/feedback/add",methods=["GET","POST"])
def show_add_feedback_page(username):
    """Shows the page for adding feedback for a logged in user
    """
    if check_session_status(username) != "authorized":
        message = common_flashes(check_session_status(username)[0])
        flash(message[0],message[1])
        return redirect(check_session_status(username)[1])
    else:
        form = FeedbackForm()
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            new_fb = Feedback(title=title,content=content,username=username)
            db.session.add(new_fb)
            db.session.commit()
            flash("New Feedback Added","alert-success")
            return redirect(f"/users/{username}")
        else:
            return render_template("add_fb_page.html",form=form)

@app.route("/feedback")
def show_feedback_page():
    """ Handles showing the page where all the feedback is displayed
    """
    fb = [feedback for feedback in Feedback.query.order_by(Feedback.id.desc()).limit(10).all()]
    fb_count = Feedback.query.count()
    return render_template("all_feedback.html",feedback=fb,fb_count=fb_count)
    
@app.route("/feedback/<int:feedback_id>/update",methods=["GET","POST"])
def update_feedback_form(feedback_id):
    """ shows the form to update feedback and handles the updating 
        of the feedback
    """
    fb = Feedback.query.get_or_404(feedback_id)
    username = fb.users.username
    if check_session_status(username) != "authorized":
        message = common_flashes(check_session_status(username)[0])
        flash(message[0],message[1])
        return redirect(check_session_status(username)[1])
    form = FeedbackForm(obj=fb)
    if form.validate_on_submit():
        fb.title = form.title.data
        fb.content = form.content.data
        db.session.commit()
        return redirect("/feedback")
    else:
        return render_template("update_feedback.html",form=form)

@app.route("/feedback/<int:feedback_id>/delete",methods=["POST"])
def delete_feedback(feedback_id):
    """Handles POST request for deleting feedback from the feedback page
    """
    fb = Feedback.query.get_or_404(feedback_id)
    username = fb.users.username
    if check_session_status(username) != "authorized":
        message = common_flashes(check_session_status(username)[0])
        flash(message[0],message[1])
        return redirect(check_session_status(username)[1])
    if delete_feedback(feedback_id):
        message = common_flashes("fb_deleted")
        flash(message[0],message[1])
    return redirect("/feedback")
        








 
        