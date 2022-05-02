from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, DateField, SelectField, HiddenField, DecimalField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError,Regexp, Optional
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flaskDemo import db
from flaskDemo.models import User, Item, Project
from wtforms.fields.html5 import DateField

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')
            
class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
    
class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')
                

                
class UpdateItemForm(FlaskForm):
    item_id = HiddenField("")
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
    submit = SubmitField("Update this item")
    
    def validate_dname(self, name):
         dept = Item.query.filter_by(name=name.data).first()
         if dept and (str(dept.item_id) != str(self.item_id.data)):
             raise ValidationError('That item name is already being used. Please choose a different name.')
            
class AddItemForm(UpdateItemForm):
    item_id = IntegerField("Item ID", validators=[DataRequired()])
    submit = SubmitField("Add Item")
    
    def validate_item_id(self, item_id):
        id = Item.query.filter_by(item_id=self.item_id.data).first()
        if id:
            raise ValidationError("That Item ID is already taken")
            
    def validate_name(self, name):
        desc = Item.query.filter_by(name=self.name.data).first()
        if desc:
            raise ValidationError("That name already exists")
            
class UpdateProjectForm(FlaskForm):
    project_id = HiddenField("")
    project_name = StringField("Name", validators=[DataRequired(), Length(min=1, max=20)])
    intent_to_sell = StringField("Intent to Sell", validators=[DataRequired(), Length(min=1, max=20)])
    description = StringField("Description", validators=[Length(max=50)])
    date_started = DateField("Date Started", format='%Y-%m-%d', validators=[Optional()])
    date_completed = DateField("Date Completed", format='%Y-%m-%d', validators=[Optional()])
    est_work_time = DecimalField("Estimated Work Time", places = 2, validators=[DataRequired()])
    submit = SubmitField("Update this project")
          
class AddProjectForm(UpdateProjectForm):
    project_id = IntegerField("Project ID", validators=[DataRequired()])
    submit = SubmitField("Add Project")
    
    def validate_project_id(self, project_id):
        proj = Project.query.filter_by(project_id=self.project_id.data).first()
        if proj:
            raise ValidationError("That Project ID is already taken")
            
class AddProjectToInventoryForm(FlaskForm):
    project_id = HiddenField("")
    item_name = HiddenField("")
    item_desc = HiddenField("")
    qtyOnHand = IntegerField("Quantity On Hand", validators=[Optional()])
    production_cost = DecimalField("Production Cost", places = 2, validators=[Optional()])
    sell_price = DecimalField("Sell Price", places = 2, validators=[Optional()])
    submit = SubmitField("Add project to inventory")