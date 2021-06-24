from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    IntegerField,
    DateField,
    TextAreaField,
)
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import InputRequired, Length, EqualTo, Email, Regexp,Optional
import email_validator
import flask_login
from flask_login import current_user
from wtforms import ValidationError
from wtforms import validators
from ..models import User


class register_form(FlaskForm):
    uname = StringField(
        validators=[
            InputRequired(),
            Length(3, 10, message="Please provide a valid name"),
            Regexp(
                "^[A-Za-z][A-Za-z0-9_.]*$",
                0,
                "Usernames must have only letters, " "numbers, dots or underscores",
            ),
        ]
    )
    email = StringField(validators=[InputRequired(), Email(), Length(1, 64)])
    pwd = PasswordField(validators=[InputRequired(), Length(8, 72)])
    cpwd = PasswordField(
        validators=[
            InputRequired(),
            Length(8, 72),
            EqualTo("pwd", message="Passwords must match !"),
        ]
    )

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError("Email already registered.")

    def validate_uname(self, uname):
        if User.query.filter_by(uname=uname.data).first():
            raise ValidationError("Username already in use.")


class login_form(FlaskForm):
    uname = StringField(
    validators=[
        InputRequired(),
        Length(3, 10, message="Please provide a valid name"),
        Regexp(
            "^[A-Za-z][A-Za-z0-9_.]*$",
            0,
            "Usernames must have only letters, " "numbers, dots or underscores",
        ),
    ]
    )
    pwd = PasswordField(validators=[InputRequired(), Length(min=8, max=72)])

    # Placeholder labels to enable form rendering
    cpwd = PasswordField(
        validators=[Optional()]
    )
    email = StringField(validators=[Optional()])



# class UpdateProfile(FlaskForm):
#     uname = StringField(
#         validators=[
#             InputRequired(),
#             Length(3, 10, message="Please provide a valid name (length of 3-10 )"),
#             Regexp(
#                 "^[A-Za-z][A-Za-z0-9_.]*$",
#                 0,
#                 "Usernames must have only letters, " "numbers, dots or underscores",
#             ),
#         ]
#     )
#     email = StringField(validators=[InputRequired(), Email(), Length(1, 64)])
#     fname = StringField(
#         validators=[
#             InputRequired(),
#             Length(3, 20, message="Please provide a valid name"),
#             Regexp(
#                 "^[A-Za-z][A-Za-z0-9_.]*$",
#                 0,
#                 "Names must have only letters, " "numbers, dots or underscores",
#             ),
#         ]
#     )
#     lname = StringField(
#         validators=[
#             InputRequired(),
#             Length(3, 20, message="Please provide a valid name"),
#             Regexp(
#                 "^[A-Za-z][A-Za-z0-9_.]*$",
#                 0,
#                 "Names must have only letters, " "numbers, dots or underscores",
#             ),
#         ]
#     )
#     about = TextAreaField()
#     profileImg = FileField(validators=[FileAllowed(["jpg", "png", "jpeg", "svg"])])

#     def validate_uname(self, uname):
#         if uname.data != current_user.uname:
#             if User.query.filter_by(uname=uname.data).first():
#                 raise ValidationError("Username already used.")

#     def validate_email(self, email):
#         if email.data != current_user.email:
#             if User.query.filter_by(email=email.data).first():
#                 raise ValidationError("Email already in use.")
