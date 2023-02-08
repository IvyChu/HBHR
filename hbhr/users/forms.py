from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, MultipleFileField
from wtforms.validators import InputRequired, Length, Email, ValidationError, Optional
from flask_security import current_user
from hbhr.models import User
from hbhr.utils import check_picture_size


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[InputRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[InputRequired(), Email()])
    display_name = StringField('Display name',
                           validators=[InputRequired(), Length(min=1, max=50)])
    notes = StringField('Bio',
                           validators=[Optional(), Length(max=160)])
    location = StringField('Location',
                           validators=[Optional(), Length(max=30)])
    
    picture = FileField('Update profile picture', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_picture(self, picture):
        check = check_picture_size(picture.data,400,400)
        if check:
            raise ValidationError("Uploaded picture is too small. Minimum dimensions are 400x400 pixels.") 

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')



class PhotoUploadForm(FlaskForm):
    photo = MultipleFileField('Upload photos', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])

