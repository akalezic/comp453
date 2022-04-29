from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, DateField, SelectField, HiddenField, DecimalField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError,Regexp
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flaskDemo import db
from flaskDemo.models import Item, Project
from wtforms.fields.html5 import DateField
            
class AddItemForm(FlaskForm):
    item_id = IntegerField("Item ID", validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired(), Length(min=1, max=50)])
    name = StringField("Item Name", validators=[DataRequired(), Length(min=1, max=20)])
    quantity = DecimalField("Quantity", places = 2, validators=[DataRequired()])
    unit = StringField("Unit", validators=[Length(max=20)])
    item_type = StringField("Item Type", validators=[DataRequired(), Length(min=1, max=10)])
    tool_condition = StringField("Tool Condition", validators=[Length(max=20)])
    color = StringField("Color", validators=[Length(max=20)])
    size = StringField("Size", validators=[Length(max=20)])
    finish = StringField("Finish", validators=[Length(max=20)])
    shape = StringField("Shape", validators=[Length(max=20)])
    submit = SubmitField("Add Item")
    
    def validate_item_id(self, item_id):
        id = Item.query.filter_by(item_id=self.item_id.data).first()
        if id:
            raise ValidationError("That Item ID is already taken")
            
    def validate_name(self, name):
        desc = Item.query.filter_by(name=self.name.data).first()
        if desc:
            raise ValidationError("That name already exists")