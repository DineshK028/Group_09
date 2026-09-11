from database import mysql
from flask import session,redirect
import re

def login_check(email,password):
    cursor=mysql.connection.cursor()
    cursor.execute("""
    select dp.delivery_id,u.user_id,u.username from users u,delivery_persons dp 
    where u.user_id=dp.user_id
    and u.email=%s and u.password_hash=%s""",(email,password))
    return cursor.fetchone()

def reset_password(email, phone, password):
    cursor = mysql.connection.cursor()
    cursor.execute("""SELECT user_id FROM users WHERE email=%s AND phone=%s AND 
    user_type='Delivery_Person' """,(email,phone)) 
    user = cursor.fetchone()
    if not user:
        return False
    cursor.execute("""
        UPDATE users SET password_hash=%s WHERE email=%s
        AND phone=%s AND user_type='Delivery_Person' """,(password,email,phone))
    mysql.connection.commit()
    return True

def get_available_orders():
    cursor = mysql.connection.cursor()
    cursor.execute("""SELECT o.order_id,o.order_number,r.name,r.address,o.delivery_address,
     o.final_amount,o.payment_status FROM 
    orders o,restaurants r where o.restaurant_id = r.restaurant_id and o.order_status in
     ('pending','out_for_delivery') AND o.order_id NOT IN 
    (SELECT order_id FROM delivery_assignments where delivery_user_id=%s and
     status in ('accepted','Rejected'))""",(session["delivery_id"],))
    return cursor.fetchall()


def accept_order(order_id,delivery_user_id):
    cursor=mysql.connection.cursor()
    cursor.execute("select * from delivery_assignments where order_id=%s and status='pending' ",(order_id,))
    if cursor.fetchone():
        cursor.close()
        return False
    cursor.execute('''insert into delivery_assignments(order_id,delivery_user_id,status) 
    values(%s,%s,'accepted')''',(order_id,delivery_user_id))
    mysql.connection.commit()
    return True

def get_active_deliveries(delivery_id):
    cursor = mysql.connection.cursor()
    cursor.execute("""SELECT
            da.assignment_id,o.order_id, o.order_number,r.name,o.delivery_address,o.final_amount,o.payment_status,da.status 
            FROM delivery_assignments da JOIN orders o ON da.order_id = o.order_id 
            JOIN restaurants r ON o.restaurant_id = r.restaurant_id 
            WHERE da.delivery_user_id=%s AND da.status IN ('accepted','picked')""", (delivery_id,))
    return cursor.fetchall()

def get_recent_activities(delivery_id):
    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT o.order_number,da.status,r.name
        FROM delivery_assignments da join orders o on  da.order_id = o.order_id
        JOIN restaurants r ON o.restaurant_id = r.restaurant_id JOIN users c ON o.user_id = c.user_id
        WHERE da.delivery_user_id = %s  AND da.status IN ('accepted','Picked', 'Delivered')  
        ORDER BY da.assignment_id DESC  LIMIT 10  """, (delivery_id,))

    return cursor.fetchall()

def get_today_earnings(delivery_id):
    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT COUNT(*) AS delivered_orders, COALESCE(SUM(o.final_amount * 0.10), 0) AS earnings 
        FROM delivery_assignments da JOIN orders o ON da.order_id = o.order_id
        WHERE da.delivery_user_id=%s AND da.status='delivered' 
        AND DATE(da.delivered_at)=CURDATE() """, (delivery_id,))
    return cursor.fetchone()

def get_last7_earnings(delivery_id):
    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT COUNT(*) AS delivered_orders, COALESCE(SUM(o.final_amount * 0.10), 0) AS earnings
        FROM delivery_assignments da JOIN orders o ON da.order_id = o.order_id
        WHERE da.delivery_user_id=%s AND da.status='delivered' 
        AND da.delivered_at >= DATE_SUB(CURDATE(), INTERVAL 7 DAY) """, (delivery_id,))
    return cursor.fetchone()

def get_alltime_earnings(delivery_id):
    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT COUNT(*) AS delivered_orders,COALESCE(SUM(o.final_amount * 0.10), 0) AS earnings 
        FROM delivery_assignments da JOIN orders o ON da.order_id = o.order_id
        WHERE da.delivery_user_id=%s AND da.status='delivered' """, (delivery_id,))
    return cursor.fetchone()



