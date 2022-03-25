from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from models.model import Users


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=20)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = Users.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')
        excluded_chars = " *?!'^+%&/()=}][{$#"
        for char in self.username.data:
            if char in excluded_chars:
                raise ValidationError(
                    f"Character {char} is not allowed in username.")

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')
        
    # def validate_password(self, password):   
    #     special_chars = " *?!'@^+%&/()=}][{$#"
    #     integers = "0123456789"
    #     lowercase = "abcdefghijklmnopqrstuvwxyz"
    #     uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        
    #     for letter in self.email.data:
    #         if letter not in special_chars:
    #             raise ValidationError("special-char")
    #         elif letter not in integers:
    #             raise ValidationError("integer")
    #         elif letter not in lowercase:
    #             raise ValidationError("lowercase")
    #         elif letter not in uppercase:
    #             raise ValidationError("uppercase")
    #         if letter not in special_chars or letter not in integers or letter not in lowercase or letter not in uppercase:
    #             raise ValidationError("The password must contain atleast 8 characters including atleast 1 integer, 1 lowercase, 1 uppercase & 1 special character(?!'^+%&/()=}][{$#")
                
class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')