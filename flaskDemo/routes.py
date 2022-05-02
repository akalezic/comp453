import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskDemo import app, db, bcrypt
from flaskDemo.models import User, Buyer, Buyer_Order, Item, Item_Order, Vendor, Project, Order_Line, Required_Items, Inventory
from flaskDemo.forms import AddItemForm, AddProjectForm, RegistrationForm, LoginForm, UpdateAccountForm, UpdateItemForm, UpdateProjectForm
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime


@app.route("/")
@app.route("/home")
def home():
    results = Item.query.all()
    vendors = Vendor.query.all()
    return render_template('home.html', outString = results, vendors=vendors)

@app.route("/projects")
def projects():
    projectsData = Project.query.all()
    return render_template('projects.html', title='Projects', outString = projectsData)
    
@app.route("/projects/<project_id>")
@login_required
def project(project_id):
    project = Project.query.get_or_404(project_id)
    return render_template('project.html', title=str(project.project_id), project=project, now=datetime.utcnow())
    
@app.route("/projects/<project_id>/update", methods=['GET', 'POST'])
@login_required
def update_project(project_id):
    project = Project.query.get_or_404(project_id)
    form = UpdateProjectForm()
    if form.validate_on_submit():
        project.project_name = form.project_name.data
        project.intent_to_sell = form.intent_to_sell.data
        project.description = form.description.data or None
        project.date_started = form.date_started.data or None
        project.date_completed = form.date_completed.data or None
        project.est_work_time = form.est_work_time.data
        db.session.commit()
        flash('The project has been updated!', 'success')
        return redirect(url_for('projects', project=project))
    elif request.method == 'GET':
        form.project_name.data = project.project_name
        form.intent_to_sell.data = project.intent_to_sell
        form.description.data = project.description
        form.date_started.data = project.date_started
        form.date_completed.data = project.date_completed
        form.est_work_time.data = project.est_work_time
    return render_template('create_project.html', title='Update Project',
                           form=form, legend='Update Project')
    
@app.route("/projects/<project_id>/delete", methods=['POST'])
@login_required
def delete_project(project_id):
    proj = Project.query.get_or_404(project_id)
    db.session.delete(proj)
    db.session.commit()
    flash('The project has been removed!', 'success')
    return redirect(url_for('projects'))

@app.route("/inventory")
def inventory():
    inventory = Inventory.query.all()
    return render_template('inventory.html', outString = inventory)

@app.route("/inventory/<project_id>")
def inve(project_id):
    inve = Inventory.query.get_or_404(project_id)
    return render_template('inve.html', inve=inve)
    
@app.route("/customerorder")
def customerorder():
    customerorder = Order_Line.query.join(Inventory,Order_Line.invID == Inventory.project_id).add_columns(Order_Line.invID, Inventory.item_desc).join(Buyer_Order, Buyer_Order.order_id == Order_Line.order_id).add_columns(Order_Line.order_id, Buyer_Order.date)
    buyers = Buyer.query.all()
    return render_template('customerorders.html', outString = customerorder, buyers=buyers)
    
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
    
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)
    
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))
    
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn
    
@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)
                           
@app.route("/item/<item_id>")
@login_required
def item(item_id):
    item = Item.query.get_or_404(item_id)
    return render_template('item.html', title=str(item.item_id), item=item, now=datetime.utcnow())
    
@app.route("/item/<item_id>/update", methods=['GET', 'POST'])
@login_required
def update_item(item_id):
    item = Item.query.get_or_404(item_id)
    form = UpdateItemForm()
    if form.validate_on_submit():
        item.description = form.description.data
        item.name = form.name.data
        item.quantity_on_hand = form.quantity.data
        item.unit = form.unit.data or None
        item.item_type = form.item_type.data
        item.tool_condition = form.tool_condition.data or None
        item.color = form.color.data or None
        item.size = form.size.data or None
        item.finish = form.finish.data or None
        item.shape = form.shape.data or None
        db.session.commit()
        flash('The item has been updated!', 'success')
        return redirect(url_for('home', item=item))
    elif request.method == 'GET':
        form.description.data = item.description
        form.name.data = item.name
        form.quantity.data = item.quantity_on_hand
        form.unit.data = item.unit
        form.item_type.data = item.item_type
        form.tool_condition.data = item.tool_condition
        form.color.data = item.color
        form.size.data = item.size
        form.finish.data = item.finish
        form.shape.data = item.shape
    return render_template('create_item.html', title='Update Item',
                           form=form, legend='Update Item')
    
@app.route("/item/<item_id>/delete", methods=['POST'])
@login_required
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash('The item has been removed!', 'success')
    return redirect(url_for('home'))
    
@app.route("/additem/new", methods=['GET', 'POST'])
@login_required
def new_item():
    form = AddItemForm()
    if form.validate_on_submit():
        add_item = Item(item_id=form.item_id.data, description=form.description.data, name=form.name.data,
                        quantity_on_hand=form.quantity.data, unit=form.unit.data or None, item_type=form.item_type.data, 
                        tool_condition=form.tool_condition.data or None, color=form.color.data or None, size=form.size.data or None,
                        finish=form.finish.data or None, shape=form.shape.data or None)
        db.session.add(add_item)
        db.session.commit()
        flash("You have added the item!", "success")
        return redirect(url_for("home"))
    return render_template("create_item.html", title="New Item", form=form, legend="New Item")    
    
@app.route("/addproject/new", methods=['GET', 'POST'])
@login_required
def new_project():
    form = AddProjectForm()
    if form.validate_on_submit():
        add_project = Project(project_id=form.project_id.data, project_name=form.project_name.data,
                              intent_to_sell=form.intent_to_sell.data, description=form.description.data or None,
                              date_started=form.date_started.data or None, date_completed=form.date_completed.data or None,
                              est_work_time=form.est_work_time.data)
        db.session.add(add_project)
        db.session.commit()
        flash("You have added the project!", "success")
        return redirect(url_for("projects"))
    return render_template("create_project.html", title="New Project", form=form, legend="New Project")