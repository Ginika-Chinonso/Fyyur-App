from datetime import datetime
from flask_wtf import FlaskForm as Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField, ValidationError
from wtforms.validators import DataRequired, AnyOf, URL
import re
from enums import Genre, State



class ShowForm(Form):
    artist_id = StringField(
        'artist_id'
    )
    venue_id = StringField(
        'venue_id'
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default= datetime.today()
    )

    def validate(self):
        rv = Form.validate(self)

        if not rv:
            return False
        
        if not is_valid_time(self.start_time):
            return False

        return True


class VenueForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=State.choices()
    )
    address = StringField(
        'address', validators=[DataRequired()]
    )
    phone = StringField(
        'phone'
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        # TODO implement enum restriction
        'genres', validators=[DataRequired()],
        choices=Genre.choices()
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL()]
    )
    website_link = StringField(
        'website_link'
    )

    seeking_talent = BooleanField( 'seeking_talent' )

    seeking_description = StringField(
        'seeking_description'
    )
    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False
        if not is_valid_phone(self.phone):
            return False
        if not is_valid_genre(self.genres):
            return False
        if not is_valid_state(self.state):
            return False
        return True
        



class ArtistForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=State.choices()
    )
    phone = StringField(
        # TODO implement validation logic for phone 
        'phone',
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        'genres', validators=[DataRequired()],
        choices=Genre.choices()
     )
    facebook_link = StringField(
        # TODO implement enum restriction
        'facebook_link', validators=[URL()]
     )

    website_link = StringField(
        'website_link'
     )

    seeking_venue = BooleanField( 'seeking_venue' )

    seeking_description = StringField(
            'seeking_description'
     )

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False
        if not is_valid_phone(self.phone):
            return False
        if not is_valid_genre(self.genres):
            return False
        if not is_valid_state(self.state):
            return False
        return True



def is_valid_phone(phone):
    us_phone_num = '^([0-9]{3})[-. ][0-9]{3}[-. ][0-9]{4}$'
    match = re.search(us_phone_num, phone.data)
    if not match:
        phone.errors.append('Invalid Phone number')
        # raise ValidationError('Error, phone number must be in format xxx-xxx-xxxx')
        return False
    return True

def is_valid_genre(genres):
    for genre in genres.data:
        if genre not in dict(Genre.choices()).keys():
            genres.errors.append('Invalid genres.')
            return False
    return True

def is_valid_state(state):
    if state.data not in dict(State.choices()).keys():
        state.errors.append('Invalid state.')
        return False
    return True

def is_valid_time(start_time):
    if start_time.data < datetime.now():
        start_time.errors.append('Invalid time')
        return False
    return True
