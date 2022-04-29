import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskDemo import app, db
from flaskDemo.models import Buyer, Buyer_Order, Item, Item_Order, Vendor, Project, Order_Line, Required_Items
from flaskDemo.forms import AddItemForm
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