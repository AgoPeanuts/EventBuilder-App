from flask_wtf import FlaskForm
from wtforms import HiddenField, DateField, SubmitField
import datetime

class EventListForm(FlaskForm):
    event_date = DateField(id='datepick', format='%Y-%m-%d')
    local_time = HiddenField('local_time')
    submit = SubmitField('Search')
