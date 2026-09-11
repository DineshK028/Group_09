from flask import render_template, request, redirect, session, flash
from delivery_module.functions import *
import re

def delivery_login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = login_check(email, password)

        if user:
            session["delivery_id"] = user[0]
            session["user_id"] = user[1]
            session["name"] = user[2]
            return redirect("delivery_dashboard")
        else:
            flash("Invalid Email or Password, If you are not registred as a Delivery Person Please contact admin")
    return render_template("delivery/login.html")

def delivery_dashboard():
    if "delivery_id" not in session:
        return redirect("/delivery/login")
    return render_template("delivery/dashboard.html")

def delivery_forgot_password():

    if request.method == "POST":
        email = request.form["email"]
        phone = request.form["phone"]
        new_password = request.form["new_password"]
        confirm_password = request.form["confirm_password"]

        # Email validation
       
        if not re.match(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$', email):
            flash("Please enter a valid email")
            return render_template("forgot_password.html")

        # Phone validation
        if not phone.isdigit() or len(phone) != 10:
            flash("Phone must be 10 digits")
            return render_template("forgot_password.html")

        # Password validation
        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{6,}$'
        if not re.match(pattern, new_password):
            flash("Password must contain uppercase, lowercase, digit and special character")
            return render_template("forgot_password.html")

        # Confirm password
        if new_password != confirm_password:
            flash("New password and confirmation do not match")
            return render_template("delivery/forgot_password.html")
        result = reset_password(email, phone, new_password)

        if result:
            flash("Password reset successful. Please login.")
            return redirect("/delivery/login")
        else:
            flash("No user found for the given email and phone")
    return render_template("delivery/forgot_password.html")


def delivery_assigned_deliveries():

    if "delivery_id" not in session:
        return redirect("/delivery/login")
    cursor=mysql.connection.cursor()
    orders = get_available_orders()
    cursor.execute('select order_id,order_status from orders')
    print(cursor.fetchall())
    print(orders)
    return render_template("delivery/assigned_deliveries.html",orders=orders)


def delivery_accept_pickup(order_id):

    if "delivery_id" not in session:
        return redirect("/delivery/login")

    success=accept_order(order_id, session["delivery_id"])
    if success:
        flash("Pick-up accepted. Head to restaurant to collect.","success")
    else:
        flash("this order was already taken by someone else","danger")
    return redirect("/delivery/assigned_deliveries")

def delivery_confirm_pickup(order_id):

    if "delivery_id" not in session:
        return redirect("/delivery/login")
    orders=get_available_orders()
    order=None
    for row in orders:
        if row[0]==order_id:
            order=row 
            break
    return render_template("delivery/confirm_pickup.html",order=order)

def delivery_reject_pickup(order_id):
    cursor=mysql.connection.cursor()
    if "delivery_id" not in session:
        return redirect("/delivery/login")  
    cursor.execute("""insert into delivery_assignments(order_id,delivery_user_id,status,rejected_at) 
    values(%s,%s,'Rejected',NOW())""", (order_id,session["delivery_id"]))
    mysql.connection.commit()  
    flash("you choose to skip this pick-up","warning")
    return redirect("/delivery/assigned_deliveries")


def delivery_order_updates():

    if "delivery_id" not in session:
        return redirect("/delivery/login")

    orders = get_active_deliveries(session["delivery_id"])
    activities = get_recent_activities(session["delivery_id"])

    return render_template("delivery/order_updates.html",orders=orders,activities=activities)

def delivery_mark_picked(assignment_id):
    cursor = mysql.connection.cursor()
    cursor.execute("""UPDATE delivery_assignments 
    SET status='Picked', picked_at=NOW() WHERE assignment_id=%s """, (assignment_id,))
    mysql.connection.commit()
    flash("Order picked from restaurant.","success")
    return redirect("/delivery/order_updates")

def delivery_reject_assignment(assignment_id):
    cursor=mysql.connection.cursor()
    cursor.execute("""DELETE FROM delivery_assignments WHERE assignment_id=%s""",(assignment_id,))
    mysql.connection.commit()
    flash("Assignment rejected and returned to pool.","warning")
    return redirect("/delivery/order_updates")

def delivery_mark_delivered(assignment_id):
    cursor=mysql.connection.cursor()
    cursor.execute("""UPDATE delivery_assignments SET status='Delivered',delivered_at=NOW()
        WHERE assignment_id=%s""",(assignment_id,))
    cursor.execute("""UPDATE orders SET order_status='delivered' WHERE order_id=
        (SELECT order_id FROM delivery_assignments
            WHERE assignment_id=%s)""",(assignment_id,))
    mysql.connection.commit()
    flash("Order delivered. Great job!","success")
    return redirect("/delivery/order_updates")

def delivery_total_earnings():

    if "delivery_id" not in session:
        return redirect(url_for("delivery_login"))

    delivery_id = session["delivery_id"]
    today = get_today_earnings(delivery_id)
    last7 = get_last7_earnings(delivery_id)
    alltime = get_alltime_earnings(delivery_id)

    return render_template("delivery/total_earnings.html",today=today,last7=last7,alltime=alltime)


def delivery_logout():
    session.clear()
    return redirect("/delivery/login")















    
