from flask_wtf import FlaskForm

from wtforms import EmailField, StringField, PasswordField, SubmitField, TelField

from wtforms.validators import DataRequired, Length, Regexp


 

class LoginForm(FlaskForm):

    email = EmailField("Email")

    password = PasswordField("Password")

    submit = SubmitField("Login")


 

class RegisterForm(FlaskForm):

    username = StringField("Username", validators=[DataRequired(), Regexp( r'^[A-Za-z]{3,10}$', message="Invalid username")])

    email = EmailField("Email", validators=[DataRequired(),Regexp(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$', message="Invalid Email")])

    password = PasswordField("Password",validators=[DataRequired(),

        Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}$',message="Password must contain uppercase, lowercase, digit and special character.")])

    phone = StringField("Phone", validators=[DataRequired(), Regexp(r'^[0-9]{10}$', message="Phone must be exactly 10 digits.")])

    address = StringField("Address", validators=[DataRequired(), Regexp(r'^[A-Za-z ]+$',message="Address should contain only letters and spaces.")])

    city = StringField("City", validators=[DataRequired(), Regexp(r'^[A-Za-z ]+$',message="City should contain only letters and spaces.")])

    zip = StringField("Zip",validators=[DataRequired(),Regexp(r'^[1-9][0-9]{5}$', message="ZIP code must be 6 digits and should not start with 0.")])

    submit = SubmitField("Register")


 

class ForgotPasswordForm(FlaskForm):

    email = EmailField("Email", validators=[DataRequired(),Regexp(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$', message="Invalid Email")])

    phone = StringField("Phone", validators=[DataRequired(), Regexp(r'^[0-9]{10}$', message="Phone must be exactly 10 digits.")])

    new_password = PasswordField("Password",validators=[DataRequired(),

        Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}$',message="Password must contain uppercase, lowercase, digit and special character.")])

    confirm_password = PasswordField("Confirm Password",validators=[DataRequired(),

        Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}$',message="Password must contain uppercase, lowercase, digit and special character.")])

    submit = SubmitField("Reset Password")
