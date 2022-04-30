from datetime import datetime
from flaskDemo import db, login_manager
from flask_login import UserMixin
from functools import partial
from sqlalchemy import orm

db.Model.metadata.reflect(db.engine)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Buyer(db.Model):
    __table__ = db.Model.metadata.tables['buyer']
    
class Buyer_Order(db.Model):
    __table__ = db.Model.metadata.tables['buyer_order']

class Item_Order(db.Model):
    __table__ = db.Model.metadata.tables['item_order']
    
class Vendor(db.Model):
    __table__ = db.Model.metadata.tables['vendor']
    
class Project(db.Model):
    __table__ = db.Model.metadata.tables['project']
    
class Item(db.Model):
    __table__ = db.Model.metadata.tables['item']

class Order_Line(db.Model):
    __table__ = db.Model.metadata.tables['order_line']
    
class Required_Items(db.Model):
    __table__ = db.Model.metadata.tables['required_items']