from datetime import datetime
from flask_login import UserMixin
from cars import db, login_manager


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), default='name')
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)
    is_staff = db.Column(db.Boolean, default=False)
    registration_time = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return '<User %r>' % self.name


def check_email_in_db(email: str) -> bool:
    user = User.query.filter_by(email=email.lower()).first()
    return True if user else False


class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # photo = picture = image_attachment('CarPhoto')
    model = db.Column(db.String(50))
    color = db.Column(db.String(50))
    number = db.Column(db.String(50))
    price_per_hour = db.Column(db.String(50))


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    price = db.Column(db.Integer, nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


