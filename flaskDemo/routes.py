import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskDemo import app, db
from flaskDemo.models import Buyer, Buyer_Order, Item, Item_Order, Vendor, Project, Order_Line, Required_Items
from flaskDemo.forms import AddItemForm, AddProjectForm
from datetime import datetime


@app.route("/")
@app.route("/home")
def home():
    results = Item.query.all()
    return render_template('home.html', outString = results)

@app.route("/about")
def about():
    projects = Project.query.all()
    return render_template('about.html', title='Projects', outString = projects)
    
@app.route("/additem/new", methods=['GET', 'POST'])
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
    return render_template("create_item.html", title="New Item", form=form)
    
@app.route("/addproject/new", methods=['GET', 'POST'])
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
        return redirect(url_for("about"))
    return render_template("create_project.html", title="New Project", form=form)