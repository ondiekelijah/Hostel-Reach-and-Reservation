from wtforms import (
    StringField,
    SelectField,
    TextField,
    PasswordField,
    BooleanField,
    IntegerField,
    DateField,
    TextAreaField,
    SelectMultipleField
)
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import InputRequired, Length, EqualTo, Email, Regexp,Optional
import email_validator
import flask_login
from flask_login import current_user
from wtforms import ValidationError
from wtforms import validators
from models import User


class UpdateProfile(FlaskForm):
    uname = StringField(
        validators=[
            InputRequired(),
            Length(3, 10, message="Please provide a valid name (length of 3-10 )"),
            Regexp(
                "^[A-Za-z][A-Za-z0-9_.]*$",
                0,
                "Usernames must have only letters, " "numbers, dots or underscores",
            ),
        ]
    )
    email = StringField(validators=[InputRequired(), Email(), Length(1, 64)])
        # Placeholder labels to enable form rendering
    cpwd = PasswordField(
        validators=[Optional()]
    )
    pwd = PasswordField(
        validators=[Optional()]
    )


    def validate_uname(self, uname):
        if uname.data != current_user.uname:
            if User.query.filter_by(uname=uname.data).first():
                raise ValidationError("Username already used.")

    def validate_email(self, email):
        if email.data != current_user.email:
            if User.query.filter_by(email=email.data).first():
                raise ValidationError("Email already in use.")




class AddHostel(FlaskForm):
    name = StringField(validators=[InputRequired(), Length(min=3, max=100)])
    # postImage = FileField(validators=[FileAllowed(["jpg", "png", "jpeg", "svg","webp"])])
    location = StringField(validators=[InputRequired(),Length(min=3, max=300)])
    management = SelectField("Management", choices=[('Markie'),('Other')])
    rooms = StringField(validators=[InputRequired(),Length(min=1, max=100)])    
    caretaker = StringField(validators=[InputRequired(),Length(min=3, max=300)])
    contact = StringField(validators=[InputRequired(),Length(10,13,message="Please provide a valid phone")])
    description = TextAreaField(validators=[InputRequired()])


class Rooms(FlaskForm):
    rent = IntegerField(validators=[InputRequired()])
    deposit = IntegerField(validators=[InputRequired()])
    amenities = SelectField(choices=[('Wifi'),('Study table'),('Bed'),('Wardrobe'),('Kitchen Shelves')])
    size = SelectField("Size", choices=[('Single'),('Bedsitter'),('1 B'),('2 B')]) 
    status = SelectField("Status", choices=[('Vacant'),('Booked'),('Occupied')])



class Search(FlaskForm):
    sval = StringField(validators=[InputRequired()])
