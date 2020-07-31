from eb import db, login_manager, bcrypt
from flask_login import UserMixin
import datetime



# User Class with UserMixin
class User(db.Model, UserMixin):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.LargeBinary(60), nullable=False)
    created = db.Column(db.DateTime, default=db.func.now())
    updated = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    event = db.relationship('Event', backref='user', cascade="all,delete", lazy=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def set_password(self, plaintext_password):
        """
        The plaine password is hashed and set to password of User Object
        """
        self.password = bcrypt.generate_password_hash(plaintext_password)

    def is_correct_password(self, password):
        """
        Check password for login
        """
        return bcrypt.check_password_hash(self.password, password)

    def __repr__(self):
        return '<User id={}, username={}, email={}, created={}>'.format(self.id, self.username, self.email, self.created)


class Event(db.Model):
    """
    Event Class
    """

    __tablename__ = 'event'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    eventname = db.Column(db.String(100), nullable=False)
    eventdate = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(255), nullable=False)
    detail = db.Column(db.Text(), nullable=False)
    public = db.Column(db.Boolean, default=True)
    created = db.Column(db.DateTime, default=db.func.now())
    updated = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    def __repr__(self):
        return '<Event id={0}, eventname={1}, eventdate={2}>'.format(self.id, self.eventname, self.eventdate)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class UserOp:
    """
    User class manipulation interface
    """
    def get_user_id(self, id):
        user = User.query.get(id)
        return user

    def get_user_email(self, email):
        user = User.query.filter_by(email=email).first()
        return user

    def get_user_name(self, username):
        user = User.query.filter_by(username=username).first()
        return user

    def add_user(self, username, email, password):
        new_user = User(username, email)
        # Call password setter
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

    def update_user(self, user):
        db.session.add(user)
        db.session.commit()

    def delete_user(self, user):
        db.session.delete(user)
        db.session.commit()


class EventOp:
    """
    Event class manipulation interface
    """
    def get_evnt_id(self, id):
        evnt = Event.query.get(id)
        return evnt

    def get_evnt_userid(self, user_id):
        evnt = Event.query.filter_by(user_id=user_id).all()
        return evnt

    def get_evnt_initial(self, eventdate):
        """
        For initial view on eventList page.
        Condition: event date equal to today or later and public
        """
        evnt = db.session.query(Event).filter(db.func.DATE(Event.eventdate)>=eventdate, Event.public==True).order_by(Event.eventdate).all()
        return evnt

    def get_evnt_join_id(self, id):
        """
        For detail view. Because username is shown, join User & Event tables.
        """
        evnt = db.session.query(Event.id, Event.eventname, Event.eventdate, Event.location, Event.detail, User.username).join(User).filter(Event.id==id).first()
        return evnt

    def add_evnt(self, event):
        db.session.add(event)
        db.session.commit()

    def delete_evnt(self, event_id):
        evnt = self.get_evnt_id(event_id)
        db.session.delete(evnt)
        db.session.commit()
