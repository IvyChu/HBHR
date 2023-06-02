from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, ValidationError, SelectMultipleField, widgets
from wtforms.validators import InputRequired, Length, URL, Email, Optional
from hbhr.utils import check_picture_size
from hbhr.models import Business
import phonenumbers 

class BusinessForm(FlaskForm):
    name = StringField('Business name', validators=[InputRequired()])
    url = StringField('Custom URL', validators=[Length(max=60, message="Webpage is limited to 60 characters.")])
    email = StringField('Business email',
                        validators=[InputRequired(), Email()])
    webpage = StringField('Webpage', validators=[Optional(), Length(max=255, message="Webpage is limited to 255 characters."),
                                                 URL(require_tld=True, message=u'Invalid URL.')])
    description = TextAreaField('Description', validators=[InputRequired()])
    image_file = FileField('Update business picture', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Submit')

    def validate_image_file(self, image_file):
        check = check_picture_size(image_file.data,400,400)
        if check:
            raise ValidationError("Uploaded picture is too small. Minimum dimensions are 400x400 pixels.") 
        
    def __init__(self, business_id=None, *args, **kwargs):
        super(BusinessForm, self).__init__(*args, **kwargs)
        self.business_id = business_id

    def validate_email(self, email):
        business = Business.query.filter_by(email=email.data).first()
        if business:
            if not business.id == self.business_id:
                raise ValidationError('Email is already in use by another business.')


class AddressForm(FlaskForm):
    address = TextAreaField('Address', validators=[InputRequired()])
    city = StringField('City', validators=[InputRequired(), Length(max=100)])
    state = StringField('State', validators=[InputRequired(), Length(max=30)])
    zip = StringField('Zip', validators=[InputRequired(), Length(max=20)])
    submit = SubmitField('Submit')

class PhoneForm(FlaskForm):
    phone_number = StringField('Phone number', validators=[InputRequired(), Length(max=40)])
    submit = SubmitField('Submit')

    def validate_phone_number(self, phone_number):
        try:
            my_number = phonenumbers.parse(f"{phone_number.data}", "US")
            check = phonenumbers.is_possible_number(my_number)
            if not check:
                raise ValidationError("This is not a phone number.") 
        except ValidationError as e:
            raise e
        except Exception as e:
            raise ValidationError("Something is wrong with this phone number.")

class LinkServicesForm(FlaskForm):
    services = SelectMultipleField('Select services your business provides', 
        coerce=int,
        option_widget=widgets.CheckboxInput(), 
        widget=widgets.ListWidget(prefix_label=False) )

    submit = SubmitField('Submit')