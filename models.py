from . import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    phone_number = db.Column(db.String(255))
    password_hash = db.Column(db.String(128))
    password_reset_token = db.Column(db.String(1000))
    rating = db.Column(db.Integer)
    def hash_password(self, password):
        return generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(255))
    code = db.Column(db.String(255))
    description = db.Column(db.String(1000))
    price = db.Column(db.Integer)
    category = db.Column(db.String(255))
    status = db.Column(db.String(20))
    image_link = db.Column(db.String(1000))
    ad_fee_paid = db.Column(db.String(3))
    location = db.Column(db.String(255))

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer)
    seller_id = db.Column(db.Integer)
    buyer_id = db.Column(db.Integer)
    title = db.Column(db.String(255))
    description = db.Column(db.String(1000))
    price = db.Column(db.Integer)
    category = db.Column(db.String(255))
    image_link = db.Column(db.String(1000))
    status = db.Column(db.String(20))
    ad_fee_paid = db.Column(db.String(3))

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))


