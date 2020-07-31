from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateTimeField, BooleanField, HiddenField
from wtforms.validators import DataRequired, Length, ValidationError
import datetime

class AddEventForm(FlaskForm):
    event_name = StringField('Event Name (Max 100 characters)', validators=[DataRequired(message='Event Name is required.'), Length(max=100)])
    event_date = DateTimeField('Event Date', id='datepick', format='%Y-%m-%d %H:%M', validators=[DataRequired(message='Event Date is required.')])
    local_time = HiddenField('local_time')
    event_location = StringField('Event Location', validators=[DataRequired(message='Event location is required.'), Length(max=255)], default='Online')
    detail = TextAreaField('Detail', validators=[DataRequired(message='Detail is required.')])
    public = BooleanField('public')

    def validate_event_date(form, field):
        # Convert datetime object with user's timezone
        event_dt = datetime.datetime.strptime(form.local_time.data, "%Y-%m-%d %H:%M:%S%z")
        # Convert the object to UTC
        event_dt_utc = event_dt.astimezone(datetime.timezone.utc)

        if event_dt_utc.date() < datetime.date.today():
            raise ValidationError("Event Date must not be earlier than today.")