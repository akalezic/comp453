from datetime import datetime
from flaskDemo import db
from functools import partial
from sqlalchemy import orm

db.Model.metadata.reflect(db.engine)





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