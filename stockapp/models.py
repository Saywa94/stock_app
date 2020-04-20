from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from stockapp import db, login

############ Declaring Models ###############
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))
    items = db.relationship('Boissons', backref='author', lazy='dynamic')

    def __repr__(self):
        return f"{self.id} <{self.username}>"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Boissons(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(60))
    quantity = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"{self.item}, {self.quantity}"

############ Login User loader Function #####
# gives Flask_login the current_user  variable
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
dj
