from flask_wtf import FlaskForm
from wtforms import StringField,FloatField,SelectField,PasswordField,TextAreaField
from wtforms.validators import InputRequired,Optional,Email,ValidationError
from models import db, connect_db,User,Feedback

class Length(object):
    """Got this length custom validator from the Flask-WTForms document site
        https://wtforms.readthedocs.io/en/2.3.x/validators/
    """
    def __init__(self, min=-1, max=-1, message=None):
        self.min = min
        self.max = max
        if not message:
            message = u'Field must be between %i and %i characters long.' % (min, max)
        self.message = message

    def __call__(self, form, field):
        l = field.data and len(field.data) or 0
        if l < self.min or self.max != -1 and l > self.max:
            raise ValidationError(self.message)
length = Length

class SignUpForm(FlaskForm):
    """Form for a user to sign-up and create an account
    """
    first_name = StringField("First Name", validators=[InputRequired(),length(max=30)])
    last_name = StringField("Last Name", validators=[InputRequired(),length(max=30)])
    email = StringField("Enter Email", validators=[InputRequired(),Email(),length(max=50)])
    username = StringField("Create A Username", validators=[InputRequired(),length(max=20)])
    password = PasswordField("Create A Password", validators=[InputRequired()])
    confirm_pass = PasswordField("Confirm Password", validators=[InputRequired()])
    
    
    def validate_confirm_pass(self,field):
        """ Custom validation function that makes sure the two passwords
            entered are the same
        """
        if field.data != self.password.data:
            raise ValidationError("Passwords Don't Match")
            
    
class LoginForm(FlaskForm):
    """Form for a user to login
    """
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    
class FeedbackForm(FlaskForm):
    """Form for adding new feedback and Updating feedback
    """
    title = StringField("Feedback Title", validators=[InputRequired(),length(max=100)])
    content = TextAreaField("Feedback Content", validators=[InputRequired(),length(max=300)])
    
class EmailConfirmationForm(FlaskForm):
    """Form for sending email to users email if they forgot password
    """
    email = StringField("Enter Email", validators=[InputRequired(),Email(),length(max=50)])
    confirm_email = StringField("Confirm Email", validators=[InputRequired(),Email(),length(max=50)])
    
    def validate_confirm_email(self,field):
        """ Custom validation function that makes sure the two emails
            entered are the same
        """
        if field.data != self.email.data:
            raise ValidationError("Emails Don't Match")

class PasswordResetForm(FlaskForm):
    """ Form for resetting user's password
    """
    password = PasswordField("Create A New Password", validators=[InputRequired()])
    confirm_pass = PasswordField("Confirm New Password", validators=[InputRequired()])
    
    def validate_confirm_pass(self,field):
        """ Custom validation function that makes sure the two passwords
            entered are the same
        """
        if field.data != self.password.data:
            raise ValidationError("Passwords Don't Match")
    

