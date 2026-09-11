from flask import render_template, redirect, flash, session, request, url_for
from customer_module.forms import LoginForm, RegisterForm, ForgotPasswordForm
from datetime import datetime, timedelta


def register_routes(app,mysql):
    @app.route("/customer/login", methods=["GET", "POST"])
    def customer_login():
        form = LoginForm()
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            if len(email)==0 or len(password)==0:
                flash("Please fill all the fields", "error")
                return redirect("/customer/login")
            cursor = mysql.connection.cursor()
            cursor.execute("select username from users where email=%s and password_hash=%s and user_type=%s", (email, password, "Customer"))
            res = cursor.fetchone()
            cursor.close()
            if res:
                cursor = mysql.connection.cursor()
                cursor.execute("select user_id, username, email, user_type, address, city, zip_code from users where email=%s and password_hash=%s and user_type=%s", (email, password, "Customer"))
                user = cursor.fetchone()
                print(user)
                cursor.close()
                
                session['user']=user
                

                print(session['user'])
                flash("Login Successful", "success")
                return redirect('/customer/dashboard')
            else:
                flash("Invalid credentials", "error")
                return redirect("/customer/login")
        return render_template("customer/login.html",form=form)

    @app.route("/customer/register", methods=['GET', 'POST'])
    def customer_register():
        form=RegisterForm()
        if form.validate_on_submit():
            username = form.username.data
            email = form.email.data
            phone = form.phone.data
            password = form.password.data
            address = form.address.data
            city = form.city.data
            zip = form.zip.data
            cursor = mysql.connection.cursor()
            cursor.execute("select email from users where email=%s", (email,))
            email_validate = cursor.fetchone()
            if email_validate:
                flash("An account with this email already exists. Please login or use a different email", "error")
                return redirect("/customer/register")
            cursor.execute("select phone from users where phone=%s", (phone,))
            phone_validator = cursor.fetchone()
            if phone_validator:
                flash("An account with this phone number already exists. Please use a different number", "error")
                return redirect("/customer/register")
            cursor.execute("insert into users(username, email, phone, password_hash, user_type, address, city, zip_code) values(%s, %s, %s, %s, %s, %s, %s, %s)", (username, email, phone, password, "Customer", address, city, zip))
            mysql.connection.commit()
            cursor.close()
            flash("Registration successful. Please login", "success")
            return redirect("/customer/login")
        return render_template("customer/register.html", form=form)

    @app.route("/customer/password/forgot", methods=['GET', 'POST'])
    def customer_forgot_password():
        form = ForgotPasswordForm()
        if form.validate_on_submit():
            email = form.email.data
            phone = form.phone.data
            new_password = form.new_password.data
            confirm_password = form.confirm_password.data
            cursor = mysql.connection.cursor()
            cursor.execute("select email from users where email=%s and phone=%s and user_type=%s", (email, phone, "Customer"))
            res = cursor.fetchone()
            cursor.close()
            print("hello")
            if res:
                if new_password==confirm_password:
                    cursor = mysql.connection.cursor()
                    cursor.execute("update users set password_hash=%s where email=%s and phone=%s", (new_password, email, phone))
                    mysql.connection.commit()
                    cursor.close()
                    flash("Password reset successful. Please login")
                    return redirect("/customer/login")
                else:
                    flash("New password and confirmation do not match")
                    return redirect("/customer/password/forgot")
            else:
                flash("No user found for the given email and phone")
                return redirect("/customer/password/forgot")
        return render_template("customer/forgot_password.html", form=form)

    @app.route("/customer/dashboard")
    def customer_dashboard():
        return render_template("customer/dashboard.html")

    @app.route("/customer/restaurants")
    def customer_restaurants():
        cursor = mysql.connection.cursor()
        cursor.execute("select name, minimum_order, delivery_fee, restaurant_id, cuisine_type, city from restaurants where is_open=%s order by restaurant_id desc", (True,))
        restaurants = cursor.fetchall()
        cursor.close()
        return render_template("customer/restaurants.html", restaurants=restaurants)


    @app.route("/customer/menu/<int:id>")
    def customer_menu(id):
        cursor = mysql.connection.cursor()
        cursor.execute("""select r.name as restaurant_name from restaurants r 
        join menu_items m on r.restaurant_id=m.restaurant_id where m.restaurant_id=%s""", (id,))
        restaurant = cursor.fetchone()
        cursor.execute(""" SELECT
            c.name, m.name, m.price, m.item_id
            FROM menu_items m JOIN menu_categories c
            ON m.category_id=c.category_id
            WHERE m.restaurant_id=%s AND m.is_available=TRUE ORDER BY c.category_id""", (id,))
        menu_items = cursor.fetchall()
        cursor.close()
        return render_template("customer/menu.html", restaurant=restaurant, menu_items=menu_items, restaurant_id=id)

    @app.route("/customer/add_to_cart", methods=["GET", "POST"])
    def customer_add_to_cart():
        if "user" not in session:
            flash("Please login to continue.", "error")
            return redirect("/customer/login")
        item_id = request.form["item_id"]
        quantity = request.form["quantity"]
        user_id = session["user"][0]
        restaurant_id = request.form["restaurant_id"]
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT restaurant_id FROM cart WHERE user_id=%s",(user_id,))
        data = cursor.fetchone()
        if data and data[0] != int(restaurant_id):
            flash("Please clear your cart before ordering from another restaurant.", "error")
            cursor.close()
            return redirect(url_for("customer_menu", id=restaurant_id))
        cursor.execute("select cart_id from cart where user_id=%s", (user_id,))
        already_cart = cursor.fetchone()
        if not already_cart:
            cursor.execute("insert into cart(user_id, restaurant_id) values(%s, %s)", (user_id, restaurant_id))
            mysql.connection.commit()
        cursor.execute("select cart_id from cart where user_id=%s", (user_id,))
        cart_id = cursor.fetchone()[0]
        cursor.execute("""select quantity from cart_items 
        where cart_id=%s and item_id=%s LIMIT 1""", (cart_id, item_id))
        exist = cursor.fetchone()
        if exist:
            qty = exist[0]+int(quantity)
            cursor.execute("update cart_items set quantity=%s where cart_id=%s and item_id=%s", (qty,cart_id, item_id))
            mysql.connection.commit()
        else:
            cursor.execute("insert into cart_items (cart_id, item_id, quantity) values(%s, %s, %s)", (cart_id, item_id, quantity))
            mysql.connection.commit()
        cursor.close()
        return redirect(url_for("customer_menu", id=restaurant_id))

    @app.route("/customer/cart")
    def customer_cart():
        user_id = session["user"][0]
        cursor = mysql.connection.cursor()
        # Restaurant Name
        cursor.execute("""SELECT r.name FROM restaurants r
            JOIN menu_items m ON r.restaurant_id = m.restaurant_id JOIN cart_items ci ON ci.item_id = m.item_id
            JOIN cart c ON c.cart_id = ci.cart_id WHERE c.user_id=%s LIMIT 1""", (user_id,))
        restaurant = cursor.fetchone()
        # Cart Items
        cursor.execute("""SELECT ci.cart_item_id, m.name, m.price, ci.quantity FROM cart_items ci
            JOIN menu_items m ON ci.item_id=m.item_id JOIN cart c ON ci.cart_id=c.cart_id WHERE c.user_id=%s """, (user_id,))
        rows = cursor.fetchall()
        cart_items = []
        total = 0
        for row in rows:
            cart_items.append({"cart_id": row[0], "item_name": row[1], "price": row[2], "quantity": row[3]})
            total += row[2] * row[3]
        cursor.close()
        return render_template("customer/cart.html", restaurant=restaurant, cart_items=cart_items, total=total)

    @app.route("/customer/remove_from_cart/<int:cart_id>", methods=["POST"])
    def customer_remove_from_cart(cart_id):
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM cart_items WHERE cart_item_id=%s", (cart_id,))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for("customer_cart"))

    @app.route("/customer/orders")
    def customer_orders():
        user_id = session["user"][0]
        cursor = mysql.connection.cursor()
        cursor.execute(""" SELECT o.order_id, r.name, o.order_status, o.final_amount, o.estimated_delivery_time
            FROM orders o JOIN restaurants r ON o.restaurant_id = r.restaurant_id
            WHERE o.user_id = %s ORDER BY o.order_id DESC""", (user_id,))
        rows = cursor.fetchall()
        orders = []
        for row in rows:
            orders.append({
                "order_id": row[0],
                "restaurant_name": row[1],
                "status": row[2],
                "final_amount": row[3],
                "eta": row[4]
            })
        cursor.close()
        return render_template("customer/orders.html", orders=orders)



    @app.route("/customer/checkout")
    def customer_checkout():
        user_id = session["user"][0]
        cursor = mysql.connection.cursor()
        # Customer Details
        cursor.execute("""SELECT username,address FROM users WHERE user_id=%s """, (user_id,))
        customer = cursor.fetchone()
        # Restaurant Name and Delivery Charge
        cursor.execute(""" SELECT r.name,r.delivery_fee
            FROM restaurants r JOIN menu_items m
                ON r.restaurant_id=m.restaurant_id
            JOIN cart_items ci
                ON ci.item_id=m.item_id
            JOIN cart c ON c.cart_id=ci.cart_id WHERE c.user_id=%s LIMIT 1 """, (user_id,))
        restaurant = cursor.fetchone()
        # Items Total
        cursor.execute(""" SELECT SUM(m.price*ci.quantity)
            FROM cart_items ci JOIN menu_items m
                ON ci.item_id=m.item_id
            JOIN cart c ON ci.cart_id=c.cart_id WHERE c.user_id=%s """, (user_id,))
        items_total = cursor.fetchone()[0]
        delivery_charge = restaurant[1]
        cursor.close()
        return render_template( "customer/checkout.html",
            customer=customer,
            restaurant=restaurant,
            items_total=items_total,
            delivery_charge=delivery_charge
        )




    @app.route("/customer/place_order", methods=["POST"])
    def customer_place_order():
        if "user" not in session:
            flash("Please login first.", "error")
            return redirect(url_for("customer_login"))
        user_id = session["user"][0]
        address = request.form["address"]
        instruction = request.form["instruction"]
        payment = request.form["payment"]
        cursor = mysql.connection.cursor()
        # Get Cart
        cursor.execute(""" SELECT cart_id, restaurant_id FROM cart WHERE user_id=%s """, (user_id,))
        cart = cursor.fetchone()
        if not cart:
            flash("Cart is empty.", "error")
            return redirect(url_for("customer_dashboard"))
        cart_id = cart[0]
        restaurant_id = cart[1]
        # Get Restaurant Details
        cursor.execute(""" SELECT minimum_order, delivery_fee FROM restaurants WHERE restaurant_id=%s """, (restaurant_id,))
        restaurant = cursor.fetchone()
        minimum_order = float(restaurant[0])
        delivery_fee = float(restaurant[1])
        # Get Cart Items
        cursor.execute(""" SELECT ci.item_id, ci.quantity, m.price, m.quantity FROM cart_items ci
            JOIN menu_items m ON ci.item_id=m.item_id WHERE ci.cart_id=%s""", (cart_id,))
        items = cursor.fetchall()
        if len(items) == 0:
            flash("Cart is empty.", "error")
            return redirect(url_for("customer_dashboard"))
        total = 0
        for item in items:
            item_id = item[0]
            qty = item[1]
            price = float(item[2])
            stock = item[3]
            if stock < qty:
                flash("Insufficient stock for an item.", "error")
                return redirect(url_for("customer_cart"))
            total += qty * price
        # Minimum Order Check
        if total < minimum_order:
            flash("Minimum order amount not met.", "error")
            return redirect(url_for("customer_checkout"))
        final_amount = total + delivery_fee
        order_number = "INFY" + datetime.now().strftime("%Y%m%d%H%M%S")
        eta = datetime.now() + timedelta(minutes=45)
        # Insert Order
        cursor.execute("""INSERT INTO orders( user_id, restaurant_id, order_number, total_amount, final_amount, 
                delivery_address, delivery_instruction, payment_method,estimated_delivery_time) VALUES
            (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
        ( user_id, restaurant_id, order_number, total, final_amount, address, instruction, payment, eta ))
        order_id = cursor.lastrowid
        # Insert Order Items
        for item in items:
            item_id = item[0]
            qty = item[1]
            price = float(item[2])
            cursor.execute("""INSERT INTO order_items( order_id, item_id, quantity, unit_price) VALUES (%s,%s,%s,%s)""",
            ( order_id, item_id, qty, price))
            cursor.execute("""UPDATE menu_items SET quantity = quantity-%s WHERE item_id=%s""",(qty, item_id))
        # Clear Cart
        cursor.execute("""DELETE FROM cart_items WHERE cart_id=%s""", (cart_id,))
        cursor.execute("""DELETE FROM cart WHERE cart_id=%s """, (cart_id,))
        mysql.connection.commit()
        cursor.close()
        flash(f"Order placed #{order_number} - ₹{final_amount}","success")
        return redirect(url_for("customer_orders"))

    @app.route("/customer/logout")
    def customer_logout():
        session.clear()
        return redirect('/')


