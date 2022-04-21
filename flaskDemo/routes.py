import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskDemo import app, db
from flaskDemo.models import Buyer, Buyer_Order, Item, Item_Order, Vendor, Project, Order_Line, Required_Items
from datetime import datetime


@app.route("/")
@app.route("/home")
def home():
    results = Item.query.all()
    return render_template('dept_home.html', outString = results)
    #posts = Employee.query.all()
    #return render_template('home.html', posts=posts)
    #results2 = Employee.query.join(Works_On,Employee.ssn == Works_On.essn) \
    #           .add_columns(Employee.ssn, Employee.fname, Employee.lname, Works_On.essn, Works_On.pno) \
    #           .join(Project, Project.pnumber == Works_On.pno).add_columns(Project.pname, Project.pnumber)
    #return render_template('join.html', title='Join', joined_m_n=results2)

   


@app.route("/about")
def about():
    return render_template('about.html', title='About')
                           
@app.route("/assign/<essn>/<pno>/delete", methods=['POST'])
def delete_assign(essn , pno):
    assign = Works_On.query.get_or_404([essn, pno])
    db.session.delete(assign)
    db.session.commit()
    flash('The employee has been removed from the project!', 'success')
    return redirect(url_for('home'))
                           
@app.route("/assign/new", methods=['GET', 'POST'])
def new_assign():
    form = EmployeeForm()
    if form.validate_on_submit():
        assign = Works_On(essn=form.ssn.data, pno=form.pnumber.data, hours=form.hours.data)
        db.session.add(assign)
        db.session.commit()
        flash('You have added the employee to the project!', 'success')
        return redirect(url_for('home'))
    return render_template('create_assign.html', title='New Assignment', form=form)

@app.route("/dept/new", methods=['GET', 'POST'])
def new_dept():
    form = DeptForm()
    if form.validate_on_submit():
        dept = Department(dname=form.dname.data, dnumber=form.dnumber.data,mgr_ssn=form.mgr_ssn.data,mgr_start=form.mgr_start.data)
        db.session.add(dept)
        db.session.commit()
        flash('You have added a new department!', 'success')
        return redirect(url_for('home'))
    return render_template('create_dept.html', title='New Department',
                           form=form, legend='New Department')


@app.route("/assign/<pno>/<essn>")
def assign(pno, essn):
    assign = Works_On.query.get_or_404([essn, pno])
    return render_template('assign.html', title=str(assign.essn) + "_" + str(assign.pno), assign=assign, now=datetime.utcnow())


@app.route("/dept/<dnumber>/update", methods=['GET', 'POST'])
def update_dept(dnumber):
    dept = Department.query.get_or_404(dnumber)
    currentDept = dept.dname

    form = DeptUpdateForm()
    if form.validate_on_submit():          # notice we are are not passing the dnumber from the form
        if currentDept !=form.dname.data:
            dept.dname=form.dname.data
        dept.mgr_ssn=form.mgr_ssn.data
        dept.mgr_start=form.mgr_start.data
        db.session.commit()
        flash('Your department has been updated!', 'success')
        return redirect(url_for('dept', dnumber=dnumber))
    elif request.method == 'GET':              # notice we are not passing the dnumber to the form

        form.dnumber.data = dept.dnumber
        form.dname.data = dept.dname
        form.mgr_ssn.data = dept.mgr_ssn
        form.mgr_start.data = dept.mgr_start
    return render_template('create_dept.html', title='Update Department',
                           form=form, legend='Update Department')
