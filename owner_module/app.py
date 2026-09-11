from flask import session,render_template,flash,request, url_for, redirect
import re

def register_routes(app,mysql):

    @app.route('/owner/login',methods=["GET","POST"])
    def owner_login():
        return render_template("owner/owner_login.html")

    @app.route("/owner/auth",methods=["GET","POST"])
    def o_login():
        if request.method=="POST":
            email=request.form["email"]
            password=request.form["password"]
            print("byeeeee")

            if not email or not password:
                flash("Please fill fields")
                return redirect(url_for("owner_login"))

            cursor=mysql.connect.cursor()
            cursor.execute("select * from  users where email=%s",(email,))
            user=cursor.fetchone()
            print(user)
            if user is None:
                flash("Invalid credentials. If you are not registered as owner, contact admoin.")
                return redirect(url_for("owner_login"))
            if password !=user[3]:
                flash("Invalid Credentials.")
                return redirect(url_for("owner_login"))
            if user[5]!="Restaurant_Owner":
                flash("Invalid Credentials.")
                return redirect(url_for("owner_login"))
            session["id"]=user[0]
            session["username"]=user[1]
            session["email"]=user[2]
            session["user_type"]=user[5]
            session["address"]=user[6]
            session["city"]=user[7]
            session["zip_code"]=user[8]
            session["phone"]=user[4]

            return redirect(url_for("owner_dashboard")) 
            
        

        # return redirect(url_for("owner_login"))
    

    @app.route("/owner/dashboard")
    def owner_dashboard():

        if "email" not in session:
            return redirect(url_for("owner_login"))
        id=session['id']
        cursor=mysql.connect.cursor()
        cursor.execute("select r.name,r.cuisine_type,r.city,r.restaurant_id,r.name from restaurants r join users u on u.user_id=r.owner_id where owner_id=%s ",(id,))
        res=cursor.fetchone()
        print(res)
        name=res[0]
        cuisine_type=res[1]
        city=res[2]
        restaurant_id=res[3]
        name=res[4]

        return render_template("owner/owner_dashboard.html",
        name=name,cuisine_type=cuisine_type,city=city,restaurant_id=restaurant_id)


    @app.route("/owner/reset-password",methods=['GET','POST'])
    def owner_reset_pass():
        return render_template("owner/password_reset.html")

    @app.route("/owner/reset",methods=['GET','POST'])
    def owner_reset_password():
        print("he")
        if request.method=="POST":
            print(request.form)
            email=request.form.get("email")
            print(email)
            phone=request.form.get("phone")
            password=request.form.get("password")
            confirm=request.form.get("confirm")

            email_pattern=r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
            if not re.match(email_pattern,email):
                flash("Please Enter a Valid email")
                return redirect("/owner/reset-password")
            phone_pattern=r'[0-9]{10}$'
            if not re.match(phone_pattern,phone):
                flash("Phone must be 10 digits")
                return redirect("/owner/reset-password")
            password_pattern=r'[A-Za-z0-9 @#$%&*()+-=_]{6,}$'
            if  not re.match(password_pattern,password):
                return redirect("/owner/reset-password")
            if password !=confirm:
                flash("New password and Confirmation do not match")
                return redirect("/owner/reset-password")
            
            cursor=mysql.connection.cursor()
            cursor.execute("select * from users where email=%s and phone=%s and user_type='Restaurant_Owner'",(email,phone))
            res=cursor.fetchone()

            if res is None:
                flash("No usre found found for given email and phone")
                return redirect("/owner/reset-password")

            cursor.execute("update users set password_hash=%s where email=%s ",(confirm,email))
            mysql.connection.commit()
            cursor.close()
            flash("Password reset successfully. Please login")
            return redirect("/owner/login")




    @app.route("/owner/category/<int:restaurant_id>")

    def owner_category_list(restaurant_id):
        print("hello123")

        conn=mysql.connection

        cur=conn.cursor()

        cur.execute(""" SELECT category_id,name FROM menu_categories WHERE restaurant_id=%s """,(restaurant_id,))

        categories=cur.fetchall()

        cur.execute("select name from restaurants where restaurant_id=%s",(restaurant_id,))
        res=cur.fetchone()
    

        return render_template("owner/category_list.html",categories=categories,restaurant_id=restaurant_id,res=res)




    @app.route("/owner/category/add/<int:restaurant_id>",

    methods=["GET","POST"])

    def owner_add_category(restaurant_id):

        if request.method=="POST":

            name=request.form["name"]

            description=request.form["description"]

            cur=mysql.connection.cursor()

            cur.execute("""

            INSERT INTO menu_categories

            (restaurant_id,name,description)

            VALUES(%s,%s,%s)

            """,(restaurant_id,name,description))

            mysql.connection.commit()

            flash("Category Added")

            return redirect(

                url_for(

                    "owner_category_list",

                    restaurant_id=restaurant_id

                )

            )

        return render_template("owner/add_category.html")

    @app.route("/owner/category/edit/<int:id>",

    methods=["GET","POST"])

    def owner_edit_category(id):

        cur=mysql.connection.cursor()

        if request.method=="POST":

            name=request.form["name"]

            description=request.form["description"]

            cur.execute("""
            UPDATE menu_categories
            SET
            name=%s,
            description=%s
            WHERE category_id=%s
            """,(name,description,id))
            mysql.connection.commit()
            flash("Category Updated")
            return redirect(url_for(
                "owner_category_list",
                restaurant_id=request.form["restaurant_id"]

            ))

        cur.execute("""

        SELECT *

        FROM menu_categories

        WHERE category_id=%s

        """,(id,))

        category=cur.fetchone()

        return render_template(

            "owner/edit_category.html",

            category=category

        )

    @app.route("/owner/category/delete/<int:id>",

    methods=["POST"])

    def owner_delete_category(id):

        restaurant_id=request.form["restaurant_id"]

        cur=mysql.connection.cursor()

        cur.execute("""

        DELETE FROM menu_categories

        WHERE category_id=%s

        """,(id,))

        mysql.connection.commit()

        flash("Category Deleted")

        return redirect(url_for(

            "owner_category_list",

            restaurant_id=restaurant_id

        ))


    @app.route('/owner/items/<int:restaurant_id>')

    def owner_items(restaurant_id):

        cur = mysql.connection.cursor()

        cur.execute(""" SELECT mi.item_id,mi.name,mc.name,mi.price,mi.is_available FROM menu_items mi 
        LEFT JOIN menu_categories mc ON mi.category_id=mc.category_id

        WHERE mi.restaurant_id=%s

        """,(restaurant_id,))

        items = cur.fetchall()
        print(items)

        cur.execute(""" SELECT name FROM restaurants WHERE restaurant_id=%s """,(restaurant_id,))

        restaurant = cur.fetchone()
        print(restaurant)

        cur.close()

        return render_template(

            "owner/items.html",

            items=items,

            restaurant=restaurant,

            restaurant_id=restaurant_id

        )


    @app.route('/owner/add_item/<int:restaurant_id>', methods=['GET', 'POST'])

    def owner_add_item(restaurant_id):

        cur = mysql.connection.cursor()

        # Load categories for dropdown

        cur.execute("""

            SELECT category_id, name

            FROM menu_categories

            WHERE restaurant_id=%s

        """, (restaurant_id,))

        categories = cur.fetchall()

        if request.method == "POST":

            category_id = request.form['category']

            name = request.form['name'].strip()

            description = request.form['description'].strip()

            price = request.form['price']

            quantity = request.form['quantity']

            ingredients = request.form['ingredients']

            vegetarian = request.form['vegetarian']

            spicy = request.form['spicy']

            available = request.form['available']

            preparation_time = request.form['preparation_time']

            # Validation

            if not re.match(r'^[A-Za-z ]+$', name):

                flash("Name should contain only letters and spaces")

                return render_template("owner/add_item.html",

                                    categories=categories,

                                    restaurant_id=restaurant_id)

            if not re.match(r'^[A-Za-z ]+$', description):

                flash("Description should contain only letters and spaces")

                return render_template("owner/add_item.html",

                                    categories=categories,

                                    restaurant_id=restaurant_id)

            if float(price) <= 0:

                flash("Price must be greater than 0")

                return render_template("owner/add_item.html",

                                    categories=categories,

                                    restaurant_id=restaurant_id)

            if int(quantity) < 0:

                flash("Quantity must be a whole number")

                return render_template("owner/add_item.html",

                                    categories=categories,

                                    restaurant_id=restaurant_id)

            cur.execute("""

            INSERT INTO menu_items

            (

            restaurant_id,

            category_id,

            name,

            description,

            price,

            quantity,

            ingredients,

            is_vegetarian,

            is_spicy,

            is_available,

            preparation_time

            )

            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)

            """,

            (

                restaurant_id,

                category_id,

                name,

                description,

                price,

                quantity,

                ingredients,

                vegetarian,

                spicy,

                available,

                preparation_time

            ))

            mysql.connection.commit()

            cur.close()

            flash("Item Added Successfully")

            return redirect(url_for('owner_items',

                                    restaurant_id=restaurant_id))

        return render_template("owner/add_item.html",categories=categories,restaurant_id=restaurant_id)





    @app.route('/owner/edit_item/<int:item_id>', methods=['GET', 'POST'])

    def owner_edit_item(item_id):

        cur = mysql.connection.cursor()

        # Get existing item

        cur.execute("""

            SELECT *

            FROM menu_items

            WHERE item_id=%s

        """, (item_id,))

        item = cur.fetchone()

        if not item:

            flash("Item not found")

            return redirect(url_for('owner_dashboard'))

        restaurant_id = item[1]      # restaurant_id

        # Load categories for dropdown

        cur.execute("""

            SELECT category_id, name

            FROM menu_categories

            WHERE restaurant_id=%s

        """, (restaurant_id,))

        categories = cur.fetchall()

        if request.method == "POST":

            category_id = request.form["category"]

            name = request.form["name"].strip()

            description = request.form["description"].strip()

            price = request.form["price"]

            quantity = request.form["quantity"]

            ingredients = request.form["ingredients"]

            vegetarian = request.form["vegetarian"]

            spicy = request.form["spicy"]

            available = request.form["available"]

            preparation_time = request.form["preparation_time"]

            # Validation

            if not re.match(r'^[A-Za-z ]+$', name):

                flash("Name should contain only letters and spaces")

                return render_template(

                    "owner/edit_item.html",

                    item=item,

                    categories=categories

                )

            if float(price) <= 0:

                flash("Price must be greater than 0")

                return render_template(

                    "owner/edit_item.html",

                    item=item,

                    categories=categories

                )

            cur.execute("""

            UPDATE menu_items

            SET

                category_id=%s,

                name=%s,

                description=%s,

                price=%s,

                quantity=%s,

                ingredients=%s,

                is_vegetarian=%s,

                is_spicy=%s,

                is_available=%s,

                preparation_time=%s

            WHERE item_id=%s

            """,

            (

                category_id,

                name,

                description,

                price,

                quantity,

                ingredients,

                vegetarian,

                spicy,

                available,

                preparation_time,

                item_id

            ))

            mysql.connection.commit()

            flash("Item Updated Successfully")

            return redirect(url_for(

                'owner_items',

                restaurant_id=restaurant_id

            ))

        return render_template(

            "owner/edit_item.html",

            item=item,

            categories=categories

        )



    @app.route('/owner/delete_item/<int:item_id>')

    def owner_delete_item(item_id):

        cur = mysql.connection.cursor()

        # Find restaurant id before deleting

        cur.execute("""

            SELECT restaurant_id

            FROM menu_items

            WHERE item_id=%s

        """, (item_id,))

        row = cur.fetchone()

        if row:

            restaurant_id = row[0]

            cur.execute("""

                DELETE FROM menu_items

                WHERE item_id=%s

            """, (item_id,))

            mysql.connection.commit()

            flash("Item Deleted Successfully")

            return redirect(url_for(

                'owner_items',

                restaurant_id=restaurant_id

            ))

        flash("Item not found")

        return redirect(url_for('owner_dashboard'))



    @app.route("/owner/orders/<int:restaurant_id>")

    def owner_orders(restaurant_id):
        print("hello")

        status = request.args.get("status")
        print(status)

        cur = mysql.connection.cursor()
        cur.execute("select name from restaurants where restaurant_id=%s",(restaurant_id,))
        name=cur.fetchone()
        print(name)

        if status and status != "all":

            cur.execute("""

            SELECT

                o.order_id,

                o.order_number,

                u.username,

                o.order_status,

                o.final_amount,

                o.estimated_delivery_time,

                o.delivered_at

            FROM orders o

            JOIN users u

            ON o.user_id=u.user_id

            WHERE o.restaurant_id=%s

            AND o.order_status=%s

            """,(restaurant_id,status))

        else:

            cur.execute("""

            SELECT

                o.order_id,

                o.order_number,

                u.username,

                o.order_status,

                o.final_amount,

                o.estimated_delivery_time,

                o.delivered_at

            FROM orders o

            JOIN users u

            ON o.user_id=u.user_id

            WHERE o.restaurant_id=%s

            """,(restaurant_id,))

        orders = cur.fetchall()
        print(orders)

        cur.close()

        return render_template(

            "owner/orders.html",
            orders=orders,
            name=name

        )

    @app.route("/owner/accept_order/<int:order_id>")

    def owner_accept_order(order_id):
       

        cur = mysql.connection.cursor()

        cur.execute("""

            UPDATE orders

            SET order_status='accepted'

            WHERE order_id=%s

        """,(order_id,))

        mysql.connection.commit()
     
        cur.close()

        return redirect(request.referrer)


    @app.route("/owner/cancel_order/<int:order_id>")

    def owner_cancel_order(order_id):
        print("rfjdked")

        cur = mysql.connection.cursor()

        cur.execute('''
            UPDATE orders SET order_status=%s
            WHERE order_id=%s''',("cancelled",order_id))

        mysql.connection.commit()

        cur.close()

        return redirect(request.referrer)



    @app.route("/owner/dispatch_order/<int:order_id>")

    def owner_dispatch_order(order_id):

        cur = mysql.connection.cursor()

        cur.execute("""

            UPDATE orders

            SET

            order_status='out_for_delivery',

            picked_up_at=NOW()

            WHERE order_id=%s

        """,(order_id,))

        mysql.connection.commit()

        cur.close()

        return redirect(request.referrer)


    @app.route("/owner/order/<int:order_id>")

    def owner_order_details(order_id):
        cur = mysql.connection.cursor()
        cur.execute(""" SELECT  o.order_number, u.user_id,u.username,u.phone,o.delivery_address,o.order_status,o.total_amount,o.discount_amount, o.final_amount

        FROM orders o
        JOIN users u
        ON o.user_id=u.user_id
        WHERE o.order_id=%s
        """,(order_id,))

        order = cur.fetchone()
        print(order)
        cur.execute("select delivery_fee from restaurants r1 inner join orders o1 on r1.restaurant_id=o1.restaurant_id where o1.order_id=%s",(order_id,))
        delivery_fee=cur.fetchone()[0]
        print(delivery_fee)
        cur.execute("""
        SELECT m.name,oi.quantity,oi.unit_price,(oi.quantity * oi.unit_price) AS item_total FROM order_items oi JOIN menu_items m 
        ON oi.item_id=m.item_id
        WHERE oi.order_id=%s
        """,(order_id,))
        items = cur.fetchall()
        order_total = sum(item[2] or 0 for item in items)
        print(order_total)
        print(items)

        if delivery_fee:
            delivery_fee=delivery_fee
        else:
            delivery_fee=20
        final_amount=order[6] + delivery_fee
        cur.close()
        return render_template("owner/order_details.html",order=order,items=items,order_total=order_total,delivery_fee=delivery_fee,final_amount=final_amount)

    @app.route('/owner/logout')
    def owner_logout():
        session.clear()
        return redirect("/owner/login")


                                                    
