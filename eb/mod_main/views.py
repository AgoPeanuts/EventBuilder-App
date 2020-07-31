from flask import Blueprint, render_template, request, Markup
from flask_login import current_user
from eb.models import Event, EventOp
from eb.mod_main.forms import EventListForm
import datetime

# create blueprint
main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    """
    Evant List for public
    """
    form = EventListForm()

    # today's date
    event_date_utc = datetime.datetime.now(datetime.timezone.utc).date()

    if request.method == 'POST':
        if form.validate_on_submit():

            # Convert datetime object with user's timezone
            event_dt = datetime.datetime.strptime(form.local_time.data, "%Y-%m-%d %H:%M:%S%z")
            # Convert the object to UTC
            event_dt_utc = event_dt.astimezone(datetime.timezone.utc)
            # Convert to date object (from datetime object)
            event_date_utc = event_dt_utc.date()

    # get event list
    evnt_list = EventOp().get_evnt_initial(event_date_utc)

    return render_template('main/index.html', form=form, evnt_list=evnt_list, current_time=datetime.datetime.utcnow())


@main.route('/event/<int:event_id>')
def detail(event_id):
    """
    Show event detail
    """
    evnt = EventOp().get_evnt_join_id(event_id)

    return render_template('main/detail.html', evnt=evnt)

