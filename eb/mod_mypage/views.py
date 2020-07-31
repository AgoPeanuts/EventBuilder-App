from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from eb.models import Event, EventOp
from eb.mod_mypage.forms import AddEventForm
import datetime

# create blueprint
mypage = Blueprint('mypage', __name__, url_prefix='/mypage')


@mypage.route('/', methods=['GET'])
@login_required
def mylist():
    """
    First view on Mypage (Show user's event list)
    """
    mylist = EventOp().get_evnt_userid(current_user.id)

    return render_template('mypage/index.html', mylist=mylist)


@mypage.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    """
    Create an event
    """
    form = AddEventForm()

    if request.method == 'POST':

        if form.validate_on_submit():

            # Convert datetime object with user's timezone
            event_dt = datetime.datetime.strptime(form.local_time.data, "%Y-%m-%d %H:%M:%S%z")
            # Convert the object to UTC
            event_dt_utc = event_dt.astimezone(datetime.timezone.utc)

            new_event = Event(
                user_id = current_user.id,
                eventname = form.event_name.data,
                eventdate = event_dt_utc,
                location = form.event_location.data,
                detail = form.detail.data,
                public = form.public.data)

            EventOp().add_evnt(new_event)
            flash('New event has been created!', 'success')
            return redirect(url_for('main.detail', event_id=new_event.id))

    return render_template('mypage/input.html', title='Create', form=form)


@mypage.route('/modify/<int:event_id>', methods=['GET', 'POST'])
@login_required
def modify(event_id):
    """
    Modify the event
    """
    form = AddEventForm()
    # get the event data by event_id
    evnt = EventOp().get_evnt_id(event_id)

    if request.method == 'POST':
        if form.validate_on_submit():

            # Convert datetime object with user's timezone
            event_dt = datetime.datetime.strptime(form.local_time.data, "%Y-%m-%d %H:%M:%S%z")
            # Convert the object to UTC
            event_dt_utc = event_dt.astimezone(datetime.timezone.utc)
            evnt.eventdate = event_dt_utc

            evnt.eventname = form.event_name.data
            evnt.location = form.event_location.data
            evnt.detail = form.detail.data
            evnt.public = form.public.data

            EventOp().add_evnt(evnt)

            flash('Your event has been changed!', 'success')
            return redirect(url_for('main.detail', event_id=evnt.id))

        return render_template('mypage/input.html', title='Modify', form=form)

    else:

        form.event_name.data = evnt.eventname
        form.local_time.data = evnt.eventdate.astimezone(datetime.timezone.utc)
        form.event_location.data = evnt.location
        form.detail.data = evnt.detail
        form.public.data = evnt.public

        return render_template('mypage/input.html', title='Modify', form=form)


@mypage.route('/delete/<int:event_id>', methods=['GET'])
@login_required
def delete(event_id):
    """
    Delete the event
    """
    EventOp().delete_evnt(event_id)

    flash('The event has been deleted.', 'success')
    return redirect(url_for('mypage.mylist'))