from flask import session, render_template, flash, redirect, url_for, request
import re
# from app import app
# from database import mysql

def register_routes(app,mysql):

    @app.route('/admin/login', methods=['GET', 'POST'])
    def admin_login():
        return render_template('admin/login.html')
    @app.route('/admin/auth', methods=['GET', 'POST'])
    def ad_login():
        if request.method == "POST":
            email = request.form['email'].strip()
            password = request.form['password']
            if email == "" or password == "":
                flash('Please fill all the fields')
                return redirect(url_for('admin_login'))
            cursor = mysql.connection.cursor()
            cursor.execute('select * from users where lower(email)=lower(%s)', (email,))
            res = cursor.fetchone()
            if res is None:
                flash('Invalid Credentials')
                return redirect(url_for('admin_login'))
            password_hash = res[3]
            user_type = res[5]
            if user_type != 'Admin':
                flash('Invalid Credentials')
                return redirect(url_for('admin_login'))
            if password != password_hash:
                flash('Invalid Credentials')
                return redirect(url_for('admin_login'))
            session['user_id'] = res[0]
            session['username'] = res[1]
            session['email'] = res[2]
            session['user_type'] = res[5]
            session['address'] = res[6]
            session['city'] = res[7]
            session['zip_code'] = res[8]
            cursor.close()
            flash('Login Successful')
            return redirect(url_for('admin_dashboard'))
        return render_template('admin/login.html')

    @app.route('/admin/dashboard')
    def admin_dashboard():
        if "user_id" not in session or session.get("user_type") != 'Admin':
            flash("Please log in as admin to continue")
            return redirect(url_for('admin_login'))
        return render_template('admin/dashboard.html', admin_name=session.get('username'))
    #MANAGE USERS
    @app.route('/admin/users')
    def admin_manage_users():
        if "user_id" not in session or session.get("user_type") != 'Admin':
            flash("Please log in as admin to continue")
            return redirect(url_for('admin_login'))
        cursor = mysql.connection.cursor()
    # FIX: was "where user_id!='Customer'" -> should filter on user_type
        cursor.execute("select user_id, username, email, phone, user_type, city from users where user_type != 'Customer' ")
        users = cursor.fetchall()
        cursor.close()
        return render_template('admin/users.html', users=users,current_user_id=session.get('user_id'))
    # ---------- ADD USER ----------
    @app.route('/admin/users/add', methods=['GET', 'POST'])
    def admin_add_user():
        if "user_id" not in session or session.get("user_type") != 'Admin':
            flash("Please log in as admin to continue")
            return redirect(url_for('admin_login'))
        if request.method == 'POST':
            username = request.form['username'].strip()
            email = request.form['email'].strip()
            password = request.form['password']
            phone = request.form['phone'].strip()
            user_type = request.form['user_type']
            address = request.form['address'].strip()
            city = request.form['city'].strip()
            zip_code = request.form.get('zip_code', '').strip()
        # Username: only alphabets and spaces, minimum 3 characters
            if not re.fullmatch(r'[A-Za-z ]{3,}', username):
                flash('Username must contain only alphabets and spaces, minimum 3 characters')
                return redirect(url_for('admin_add_user'))
        # Email: valid format
            if not re.fullmatch(r'[^@\s]+@[^@\s]+\.[a-zA-Z]{2,}', email):
                flash('Invalid email format')
                return redirect(url_for('admin_add_user'))
        # Password: min 6, upper, lower, digit, special char
            if not re.fullmatch(r'(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=]).{6,}', password):
                flash('''Password must be at least 6 characters with uppercase, 
                lowercase, digit, and special character''')
                return redirect(url_for('admin_add_user'))
        # Phone: 10 digits starting with 6-9
            if not re.fullmatch(r'[6-9][0-9]{9}', phone):
                flash('Phone must be 10 digits starting with 6, 7, 8, or 9')
                return redirect(url_for('admin_add_user'))
        # User type
            if user_type not in ('Admin', 'Restaurant_Owner', 'Delivery_Person'):
                flash('User Type must be one of: Admin, Restaurant_Owner, Delivery_Person')
                return redirect(url_for('admin_add_user'))

        # Address: letters, numbers, spaces, commas, hyphens, periods, slashes, hashes
        # FIX: original regex was malformed (unescaped hyphen created a broken range, missing closing bracket)
            if not re.fullmatch(r'[A-Za-z0-9 ,./#-]+', address):
                flash('Address contains invalid characters')
                return redirect(url_for('admin_add_user'))

        # City: letters/spaces, min 3
            if not re.fullmatch(r'[A-Za-z ]{3,}', city):
                flash('City must contain only letters/spaces, minimum 3 characters')
                return redirect(url_for('admin_add_user'))

        # Zip code: optional, 6-digit Indian PIN not starting with 0
            if zip_code and not re.fullmatch(r'[1-9][0-9]{5}', zip_code):
                flash('ZIP Code must be a 6-digit Indian PIN not starting with 0')
                return redirect(url_for('admin_add_user'))

            cursor = mysql.connection.cursor()

        # Duplicate email check
            cursor.execute('select * from users where lower(email)=lower(%s)', (email,))
            if cursor.fetchone():
                flash('Email is already present. Please use a different email.')
                cursor.close()
                return redirect(url_for('admin_add_user'))

        # Duplicate phone check (phone column is UNIQUE in schema)
            cursor.execute('select * from users where phone=%s', (phone,))
            if cursor.fetchone():
                flash('This phone number is already registered with another user.')
                cursor.close()
                return redirect(url_for('admin_add_user'))

        # Delivery_Person specific fields
            vehicle_type = vehicle_number = license_number = None
            if user_type == 'Delivery_Person':
                vehicle_type = request.form.get('vehicle_type', '').strip()
                vehicle_number = request.form.get('vehicle_number', '').strip()
                license_number = request.form.get('license_number', '').strip()

                if not vehicle_type:
                    flash('Vehicle Type is required for Delivery Person')
                    cursor.close()
                    return redirect(url_for('admin_add_user'))

                if not re.fullmatch(r'[A-Z]{2}-\d{2}-[A-Z]{2}-\d{4}', vehicle_number):
                    flash('Vehicle Number must be in format KA-01-AB-1234')
                    cursor.close()
                    return redirect(url_for('admin_add_user'))

            # FIX: format per spec is "KA 01-2020-1234567" (space after state code, not hyphen)
                if not re.fullmatch(r'[A-Z]{2}-\d{2}-\d{4}-\d{7}', license_number):
                    flash('License Number must be in format KA 01-2020-1234567')
                    cursor.close()
                    return redirect(url_for('admin_add_user'))

            # FIX: this is a NEW user being created, so there's no user_id yet to exclude
                cursor.execute('select * from delivery_persons where license_number=%s', (license_number,))
                if cursor.fetchone():
                    flash('This license number is already used by another delivery person.')
                    cursor.close()
                    return redirect(url_for('admin_add_user'))

            cursor.execute(
            'insert into users (username, email, password_hash, phone, user_type, address, city, zip_code) '
            'values (%s,%s,%s,%s,%s,%s,%s,%s)',
            (username, email, password, phone, user_type, address, city, zip_code or None)
            )
            new_user_id = cursor.lastrowid

        # FIX: table name typo "dleivery_persons" -> "delivery_persons"
            if user_type == 'Delivery_Person':
                cursor.execute(
                'insert into delivery_persons (user_id, vehicle_type, vehicle_number, license_number) '
                'values (%s,%s,%s,%s)',
                (new_user_id, vehicle_type, vehicle_number, license_number)
                )

            mysql.connection.commit()
            cursor.close()

            flash('User added successfully')
            return redirect(url_for('admin_manage_users'))

        return render_template('admin/add_user.html')


    # ---------- EDIT USER ----------
    @app.route('/admin/users/edit/<int:user_id>', methods=['GET', 'POST'])
    def admin_edit_user(user_id):
        if "user_id" not in session or session.get("user_type") != 'Admin':
            flash("Please log in as admin to continue")
            return redirect(url_for('admin_login'))

        cursor = mysql.connection.cursor()
        cursor.execute('select * from users where user_id=%s', (user_id,))
        user = cursor.fetchone()

        if user is None:
            cursor.close()
            flash('User not found')
            return redirect(url_for('admin_manage_users'))

        if request.method == 'POST':
            username = request.form['username'].strip()
            email = request.form['email'].strip()
            phone = request.form['phone'].strip()
            address = request.form['address'].strip()
            city = request.form['city'].strip()
            zip_code = request.form.get('zip_code', '').strip()
        # Role is NOT editable — always use the original value from DB
            user_type = user[5]

            if not re.fullmatch(r'[A-Za-z ]{3,}', username):
                flash('Username must contain only alphabets and spaces, minimum 3 characters')
                cursor.close()
                return redirect(url_for('admin_edit_user', user_id=user_id))

            if not re.fullmatch(r'[^@\s]+@[^@\s]+\.[a-zA-Z]{2,}', email):
                flash('Invalid email format')
                cursor.close()
                return redirect(url_for('admin_edit_user', user_id=user_id))

            if not re.fullmatch(r'[6-9][0-9]{9}', phone):
                flash('Phone must be 10 digits starting with 6, 7, 8, or 9')
                cursor.close()
                return redirect(url_for('admin_edit_user', user_id=user_id))

        # FIX: same malformed regex as add_user, now corrected
            if not re.fullmatch(r'[A-Za-z0-9 ,./#-]+', address):
                flash('Address contains invalid characters')
                cursor.close()
                return redirect(url_for('admin_edit_user', user_id=user_id))

            if not re.fullmatch(r'[A-Za-z ]{3,}', city):
                flash('City must contain only letters/spaces, minimum 3 characters')
                cursor.close()
                return redirect(url_for('admin_edit_user', user_id=user_id))

            if zip_code and not re.fullmatch(r'[1-9][0-9]{5}', zip_code):
                flash('ZIP Code must be a 6-digit Indian PIN not starting with 0')
                cursor.close()
                return redirect(url_for('admin_edit_user', user_id=user_id))

        # Duplicate email check (excluding self)
            cursor.execute('select * from users where lower(email)=lower(%s) and user_id!=%s', (email, user_id))
            if cursor.fetchone():
                flash('Email is already present. Please use a different email.')
                cursor.close()
                return redirect(url_for('admin_edit_user', user_id=user_id))

        # Duplicate phone check (excluding self)
            cursor.execute('select * from users where phone=%s and user_id!=%s', (phone, user_id))
            if cursor.fetchone():
                flash('This phone number is already registered with another user.')
                cursor.close()
                return redirect(url_for('admin_edit_user', user_id=user_id))

            cursor.execute(
            'update users set username=%s, email=%s, phone=%s, address=%s, city=%s, zip_code=%s where user_id=%s',
            (username, email, phone, address, city, zip_code or None, user_id)
            )

            if user_type == 'Delivery_Person':
                vehicle_type = request.form.get('vehicle_type', '').strip()
                vehicle_number = request.form.get('vehicle_number', '').strip()
                license_number = request.form.get('license_number', '').strip()

                if not re.fullmatch(r'[A-Z]{2}-\d{2}-[A-Z]{2}-\d{4}', vehicle_number):
                    flash('Vehicle Number must be in format KA-01-AB-1234')
                    cursor.close()
                    return redirect(url_for('admin_edit_user', user_id=user_id))

            # FIX: format per spec is "KA 01-2020-1234567"
                if not re.fullmatch(r'[A-Z]{2}-\d{2}-\d{4}-\d{7}', license_number):
                    flash('License Number must be in format KA-01-2020-1234567')
                    cursor.close()
                    return redirect(url_for('admin_edit_user', user_id=user_id))

                cursor.execute('select * from delivery_persons where license_number=%s and user_id!=%s', (license_number, user_id))
                if cursor.fetchone():
                    flash('This license number is already used by another delivery person.')
                    cursor.close()
                    return redirect(url_for('admin_edit_user', user_id=user_id))

            
                cursor.execute(
                'update delivery_persons set vehicle_type=%s, vehicle_number=%s, license_number=%s where user_id=%s',
                (vehicle_type, vehicle_number, license_number, user_id)
                )

            mysql.connection.commit()
            cursor.close()
            flash('User updated successfully')
            return redirect(url_for('admin_manage_users'))

    
        delivery_info = None
        if user[5] == 'Delivery_Person':
            cursor.execute('select * from delivery_persons where user_id=%s', (user_id,))
            delivery_info = cursor.fetchone()  
        cursor.close()
        return render_template('admin/edit_user.html', user=user, delivery_info=delivery_info)


    #DELETE USER

    @app.route('/admin/users/delete/<int:user_id>', methods=['POST'])
    def admin_delete_user(user_id):
        if "user_id" not in session or session.get("user_type") != 'Admin':
            flash("Please log in as admin to continue")
            return redirect(url_for('admin_login'))

        if user_id == session['user_id']:
            flash('You cannot delete your own account')
            return redirect(url_for('admin_manage_users'))

        cursor = mysql.connection.cursor()
        cursor.execute('delete from users where user_id=%s', (user_id,))
        mysql.connection.commit()
        cursor.close()

        flash('User deleted successfully')
        return redirect(url_for('admin_manage_users'))


    # MANAGE RESTAURANTS (LIST) 
    @app.route('/admin/restaurants')
    def admin_manage_restaurants():
        if "user_id" not in session or session.get("user_type") != 'Admin':
            flash("Please log in as admin to continue")
            return redirect(url_for('admin_login'))
        cursor = mysql.connection.cursor()
        cursor.execute("select count(*) from users where user_type='Restaurant_Owner'")
        owner_count = cursor.fetchone()[0]
        cursor.execute('''select r.restaurant_id, r.name, u.username, r.cuisine_type, r.city, r.is_open 
        from restaurants r join users u on r.owner_id = u.user_id''')
        restaurants = cursor.fetchall()
        cursor.close()
        return render_template('admin/restaurants.html', restaurants=restaurants, owner_count=owner_count, admin_name=session.get('username'))

    # ADD RESTAURANT 
    @app.route('/admin/restaurants/add', methods=['GET', 'POST'])
    def admin_add_restaurant():
        if "user_id" not in session or session.get("user_type") != 'Admin':
            flash("Please log in as admin to continue")
            return redirect(url_for('admin_login'))

        cursor = mysql.connection.cursor()
        cursor.execute("select user_id, username from users where user_type='Restaurant_Owner'")
        owners = cursor.fetchall()

        if not owners:
            cursor.close()
            flash("No Restaurant Owner exists. Please add an Owner first.")
            return redirect(url_for('admin_add_user'))

        if request.method == 'POST':
            owner_id = request.form['owner_id']
            name = request.form['name'].strip()
            cuisine_type = request.form['cuisine_type'].strip()
            address = request.form['address'].strip()
            city = request.form['city'].strip()
            zip_code = request.form.get('zip_code', '').strip()
            contact_phone = request.form['contact_phone'].strip()
            contact_email = request.form['contact_email'].strip()
            delivery_fee = request.form.get('delivery_fee', '').strip()
            minimum_order = request.form.get('minimum_order', '').strip()

            # Letters-only fields
            if not re.fullmatch(r'[A-Za-z ]+', name):
                flash('Restaurant Name must contain only letters and spaces')
                cursor.close()
                return redirect(url_for('admin_add_restaurant'))

            if not re.fullmatch(r'[A-Za-z ]+', cuisine_type):
                flash('Cuisine Type must contain only letters and spaces')
                cursor.close()
                return redirect(url_for('admin_add_restaurant'))

            if not re.fullmatch(r'[A-Za-z ]+', address):
                flash('Address must contain only letters and spaces')
                cursor.close()
                return redirect(url_for('admin_add_restaurant'))

            if not re.fullmatch(r'[A-Za-z ]+', city):
                flash('City must contain only letters and spaces')
                cursor.close()
                return redirect(url_for('admin_add_restaurant'))

            # Phone
            if not re.fullmatch(r'[6-9][0-9]{9}', contact_phone):
                flash('Contact Phone must be 10 digits starting with 6, 7, 8, or 9')
                cursor.close()
                return redirect(url_for('admin_add_restaurant'))

            # Email format
            if not re.fullmatch(r'[^@\s]+@[^@\s]+\.[a-zA-Z]{2,}', contact_email):
                flash('Invalid email format')
                cursor.close()
                return redirect(url_for('admin_add_restaurant'))

            # ZIP optional, 6 digits not starting with 0
            if zip_code and not re.fullmatch(r'[1-9][0-9]{5}', zip_code):
                flash('ZIP Code must be 6 digits not starting with 0')
                cursor.close()
                return redirect(url_for('admin_add_restaurant'))

            # Delivery fee
            try:
                delivery_fee = float(delivery_fee) if delivery_fee else 15.00
                if delivery_fee <= 0:
                    raise ValueError
            except ValueError:
                flash('Delivery Fee must be a positive value')
                cursor.close()
                return redirect(url_for('admin_add_restaurant'))

            # Minimum order
            try:
                if minimum_order and not minimum_order.isdigit():
                    raise ValueError
                minimum_order = int(minimum_order) if minimum_order else 1
                if minimum_order < 1:
                    raise ValueError
            except ValueError:
                flash('Minimum Order must be 1 or more')
                cursor.close()
                return redirect(url_for('admin_add_restaurant'))

            # Duplicate email check
            cursor.execute('select * from restaurants where contact_email=%s', (contact_email,))
            if cursor.fetchone():
                flash('A restaurant with this contact email already exists.')
                cursor.close()
                return redirect(url_for('admin_add_restaurant'))

            # Duplicate name+owner check
            cursor.execute('select * from restaurants where name=%s and owner_id=%s', (name, owner_id))
            if cursor.fetchone():
                flash('This owner already has a restaurant with this name.')
                cursor.close()
                return redirect(url_for('admin_add_restaurant'))

            cursor.execute(
                '''insert into restaurants (owner_id, name, cuisine_type, address, city, zip_code,
                contact_phone, contact_email, delivery_fee, minimum_order) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
                (owner_id, name, cuisine_type, address, city, zip_code or None,
                contact_phone, contact_email, delivery_fee, minimum_order)
            )
            mysql.connection.commit()
            cursor.close()

            flash('Restaurant added')
            return redirect(url_for('admin_manage_restaurants'))

        cursor.close()
        return render_template('admin/add_restaurant.html', owners=owners, admin_name=session.get('username'))
    

    # EDIT RESTAURANT

    @app.route('/admin/restaurants/edit/<int:restaurant_id>', methods=['GET', 'POST'])
    def admin_edit_restaurant(restaurant_id):
        if "user_id" not in session or session.get("user_type") != 'Admin':
            flash("Please log in as admin to continue")
            return redirect(url_for('admin_login'))
        cursor = mysql.connection.cursor()
        cursor.execute('select * from restaurants where restaurant_id=%s', (restaurant_id,))
        restaurant = cursor.fetchone()
        if restaurant is None:
            cursor.close()
            flash('Restaurant not found')
            return redirect(url_for('admin_manage_restaurants'))

        cursor.execute("select user_id, username from users where user_type='Restaurant_Owner'")
        owners = cursor.fetchall()

        if request.method == 'POST':
            owner_id = request.form['owner_id']
            name = request.form['name'].strip()
            cuisine_type = request.form['cuisine_type'].strip()
            address = request.form['address'].strip()
            city = request.form['city'].strip()
            zip_code = request.form.get('zip_code', '').strip()
            contact_phone = request.form['contact_phone'].strip()
            contact_email = request.form['contact_email'].strip()
            delivery_fee = request.form.get('delivery_fee', '').strip()
            minimum_order = request.form.get('minimum_order', '').strip()
            is_open = 1 if request.form.get('is_open') == '1' else 0
            if not re.fullmatch(r'[A-Za-z ]+', name):
                flash('Restaurant Name must contain only letters and spaces')
                cursor.close()
                return redirect(url_for('admin_edit_restaurant', restaurant_id=restaurant_id))
            if not re.fullmatch(r'[A-Za-z ]+', cuisine_type):
                flash('Cuisine Type must contain only letters and spaces')
                cursor.close()
                return redirect(url_for('admin_edit_restaurant', restaurant_id=restaurant_id))
                # Address accepts letters, numbers, spaces, commas, hyphens, periods, slashes, and hashes 
            if not re.fullmatch(r'[A-Za-z ]+', address):
                flash('Address must contain only letters and spaces')
                cursor.close()
                return redirect(url_for('admin_edit_restaurant', restaurant_id=restaurant_id))
            if not re.fullmatch(r'[A-Za-z ]+', city):
                flash('City must contain only letters and spaces')
                cursor.close()
                return redirect(url_for('admin_edit_restaurant', restaurant_id=restaurant_id))
            if not re.fullmatch(r'[6-9][0-9]{9}', contact_phone):
                flash('Contact Phone must be 10 digits starting with 6, 7, 8, or 9')
                cursor.close()
                return redirect(url_for('admin_edit_restaurant', restaurant_id=restaurant_id))
            if not re.fullmatch(r'[^@\s]+@[^@\s]+\.[a-zA-Z]{2,}', contact_email):
                flash('Invalid email format')
                cursor.close()
                return redirect(url_for('admin_edit_restaurant', restaurant_id=restaurant_id))
            if zip_code and not re.fullmatch(r'[1-9][0-9]{5}', zip_code):
                flash('ZIP Code must be 6 digits not starting with 0')
                cursor.close()
                return redirect(url_for('admin_edit_restaurant', restaurant_id=restaurant_id))
            try:
                delivery_fee = float(delivery_fee)
                if delivery_fee <= 0:
                    raise ValueError
            except ValueError:
                flash('Delivery Fee must be a positive value')
                cursor.close()
                return redirect(url_for('admin_edit_restaurant', restaurant_id=restaurant_id))
            try:
                minimum_order = float(minimum_order)
                if minimum_order < 1:
                    raise ValueError
            except ValueError:
                flash('Minimum Order must be 1 or more')
                cursor.close()
                return redirect(url_for('admin_edit_restaurant', restaurant_id=restaurant_id))
            cursor.execute('select * from restaurants where contact_email=%s and restaurant_id!=%s', 
            (contact_email, restaurant_id))
            if cursor.fetchone():
                flash('A restaurant with this contact email already exists.')
                cursor.close()
                return redirect(url_for('admin_edit_restaurant', restaurant_id=restaurant_id))
            cursor.execute('''update restaurants set owner_id=%s, name=%s, cuisine_type=%s, address=%s,
            city=%s, zip_code=%s, contact_phone=%s, contact_email=%s, 
            delivery_fee=%s, minimum_order=%s, is_open=%s where restaurant_id=%s''', 
            (owner_id, name, cuisine_type, address, city, zip_code or None, contact_phone, 
            contact_email, delivery_fee, minimum_order, is_open, restaurant_id))
            mysql.connection.commit()
            cursor.close()
            flash('Restaurant updated')
            return redirect(url_for('admin_manage_restaurants'))
        cursor.close()
        return render_template('admin/edit_restaurant.html', restaurant=restaurant, 
        owners=owners, admin_name=session.get('username'))

    

    # DELETE RESTAURANT

    @app.route('/admin/restaurants/delete/<int:restaurant_id>', methods=['POST'])

    def admin_delete_restaurant(restaurant_id):

        if "user_id" not in session or session.get("user_type") != 'Admin':

            flash("Please log in as admin to continue")

            return redirect(url_for('admin_login'))

        cursor = mysql.connection.cursor()

        cursor.execute('delete from restaurants where restaurant_id=%s', (restaurant_id,))

        mysql.connection.commit()

        cursor.close()

        flash('Restaurant deleted')

        return redirect(url_for('admin_manage_restaurants'))
        

    @app.route('/admin/profile')
    def admin_profile():

        if "user_id" not in session or session.get("user_type") != "Admin":
            flash("Please log in as admin to continue")
            return redirect(url_for('admin_login'))

        cursor = mysql.connection.cursor()

        cursor.execute("""
            SELECT username, email, phone, user_type, address, city, zip_code
            FROM users
            WHERE user_id=%s
        """, (session['user_id'],))

        admin = cursor.fetchone()

        cursor.close()

        if not admin:
            flash("Profile not found")
            return redirect(url_for('admin_dashboard'))

        return render_template(
            'admin/admin_profile.html',
            admin=admin,
            admin_name=session.get('username')
        )


    @app.route('/admin/change-password', methods=['GET', 'POST'])
    def admin_change_password():

        if "user_id" not in session or session.get("user_type") != "Admin":
            flash("Please log in as admin to continue")
            return redirect(url_for('admin_login'))

        if request.method == "POST":

            current_password = request.form['current_password']
            new_password = request.form['new_password']
            confirm_password = request.form['confirm_password']

            if not current_password or not new_password or not confirm_password:
                flash("All fields are mandatory")
                return redirect(url_for('admin_change_password'))

            pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}$'

            if not re.fullmatch(pattern, new_password):
                flash("New Password must contain at least 6 characters including uppercase, lowercase, digit and special character")
                return redirect(url_for('admin_change_password'))

            if new_password != confirm_password:
                flash("New password and Confirm password do not match")
                return redirect(url_for('admin_change_password'))

            cursor = mysql.connection.cursor()

            cursor.execute(
                "SELECT password_hash FROM users WHERE user_id=%s",
                (session['user_id'],)
            )

            result = cursor.fetchone()

            if not result:
                cursor.close()
                flash("User not found")
                return redirect(url_for('admin_login'))

            db_password = result[0]

            if current_password != db_password:
                cursor.close()
                flash("Current password is incorrect")
                return redirect(url_for('admin_change_password'))

            if new_password == current_password:
                cursor.close()
                flash("New password must be different from the current password")
                return redirect(url_for('admin_change_password'))

            cursor.execute(
                "UPDATE users SET password_hash=%s WHERE user_id=%s",
                (new_password, session['user_id'])
            )

            mysql.connection.commit()
            cursor.close()

            flash("Password updated successfully.")
            return redirect(url_for('admin_profile'))

        return render_template(
            'admin/change_password.html',
            admin_name=session.get('username')
        )



    #  restrict to POST only, matching the form-based logout button in dashboard.html/users.html
    @app.route('/admin/logout', methods=['GET','POST'])
    def admin_logout():
        session.clear()
        flash('Logged out successfully')
        return redirect(url_for('admin_login'))

