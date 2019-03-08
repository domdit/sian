from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SubmitField, BooleanField, PasswordField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from siamsite.models import User


class Login(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class NewAdmin(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Create New Admin')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class NewItem(FlaskForm):
    name = StringField('Item Name', validators=[DataRequired()])
    description = TextAreaField('Item Description')
    img = FileField('Add Image?', validators=[FileAllowed(['jpg', 'png', 'gif'])])
    head = BooleanField('Heading')
    spice = BooleanField('Spicy')
    veg = BooleanField('Vegetarian')
    submit = SubmitField('Add Item')


class NewCaterItem(FlaskForm):
    name = StringField('Item Name', validators=[DataRequired()])
    description = TextAreaField('Item Description')
    whole = StringField('Whole Price')
    half = StringField('Half Price')
    head = BooleanField('Heading')
    spice = BooleanField('Spicy')
    veg = BooleanField('Vegetarian')
    submit = SubmitField('Add Item')


class NewEvent(FlaskForm):
    name = StringField('Item Name', validators=[DataRequired()])
    description = TextAreaField('Item Description')
    location = StringField('Location')
    date = DateField('Date', format='%m/%d/%Y')
    start_time = StringField('Start')
    end_time = StringField('End')
    submit = SubmitField('Add Item')


class Image(FlaskForm):
    img1 = FileField('Image Uploader 1', validators=[FileAllowed(['jpg', 'png', 'gif'])])
    img2 = FileField('Image Uploader 2', validators=[FileAllowed(['jpg', 'png', 'gif'])])
    img3 = FileField('Image Uploader 3', validators=[FileAllowed(['jpg', 'png', 'gif'])])
    img4 = FileField('Image Uploader 4', validators=[FileAllowed(['jpg', 'png', 'gif'])])
    submit = SubmitField('Upload Images')


class Contact(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=6, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    subject = StringField('Subject')
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send Email')
