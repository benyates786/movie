from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog import mongo
from flask import session


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()]
                        )
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        users = mongo.db.users
        existing_user = users.find_one({'name': username.data})
        if existing_user:
            raise ValidationError(
                'That username is taken. Please choose a different one.')

    def validate_email(self, email):
        users = mongo.db.users
        existing_user = users.find_one({'email': email.data})
        if existing_user:
            raise ValidationError(
                'That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[
                        FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != session['username']:
            users = mongo.db.users
            user = users.find_one({'name': username.data})
            if user:
                raise ValidationError(
                    'That username is taken. Please choose a different one.')

    def validate_email(self, email):
        users = mongo.db.users
        user = users.find_one({'name': session['username']})
        if email.data != user['email']:
            user = users.find_one({'email': email.data})
            if user:
                raise ValidationError(
                    'That email is taken. Please choose a different one.')


class PostForm(FlaskForm):
    title = StringField('Movie Name', validators=[DataRequired()])
    link = TextAreaField('Movie Poster', validators=[DataRequired()])
    review = TextAreaField('Movie Review')
    content = TextAreaField('Movie Description', validators=[DataRequired()])

    submit = SubmitField('Post')
