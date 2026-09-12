# 🍔 Food Express

> 🚀 **A modular Flask-based food delivery web application** with dedicated workflows for Customers, Restaurant Owners, Delivery Personnel, and Administrators.

<p align="center">

**🌐 Live Demo:** [Food Express](https://group-09.onrender.com)

</p>

---

## ✨ Features

### 👤 Customer
- 🔐 Customer registration and login
- 🍽️ Browse restaurants and menu items
- 🛒 Add items to cart
- ➕➖ Manage cart quantities
- 📦 Place orders
- 📍 View order information and status

### 🏪 Restaurant Owner
- 🏬 Restaurant management
- 📋 Menu and category management
- 📦 View and manage orders

### 🛵 Delivery Personnel
- 🔐 Delivery-person login
- 📊 Delivery dashboard
- 📦 View assigned deliveries
- ✅ Accept/reject delivery assignments
- 📍 Confirm pickup
- 🔄 Update delivery status
- 💰 View total earnings
- 📝 Track delivery events

### 🛡️ Admin
- 👨‍💼 Administrative module
- 👥 User management
- 📊 Application data management

---

## 🧰 Technology Stack

| Technology | Purpose |
|---|---|
| 🐍 **Python** | Programming language |
| 🌶️ **Flask** | Web framework |
| 🗄️ **MySQL / MariaDB** | Database |
| 🔌 **Flask-MySQLdb** | Database connectivity |
| 🎨 **HTML / CSS** | Frontend |
| 🧩 **Jinja2** | Templates |
| 🚀 **Gunicorn** | Production WSGI server |
| ☁️ **Render** | Application hosting |
| 🛢️ **Aiven MySQL** | Cloud database |
| 💻 **XAMPP** | Local development database |

---

## 📁 Project Structure

```text
Food_Express/
│
├── 📂 admin_module/
│   └── admin_routes.py
│
├── 📂 customer_module/
│   ├── app.py
│   └── forms.py
│
├── 📂 delivery_module/
│   ├── functions.py
│   ├── main.py
│   └── routes.py
│
├── 📂 owner_module/
│   └── app.py
│
├── 📂 static/
│   ├── 📂 customer/
│   │   └── style.css
│   └── 📂 delivery/
│       ├── assigned_deliveries.css
│       ├── confirm_pickup.css
│       ├── dashboard.css
│       ├── forgot_password.css
│       ├── login.css
│       ├── order_updates.css
│       └── total_earnings.css
│
├── 📂 templates/
│   ├── admin/
│   ├── customer/
│   ├── delivery/
│   ├── owner/
│   └── index.html
│
├── app.py
├── database.py
└── requirements.txt
```

---

## 🚀 Live Demo

🔗 **[Open Food Express](https://group-09.onrender.com)**

> 💡 The application is hosted on Render. Free hosting instances may take a short time to wake up after inactivity.

---

## 💻 Local Setup

### 1️⃣ Clone the Repository

```bash
git clone <your-repository-url>
cd Food_Express
```

### 2️⃣ Create a Virtual Environment

```bash
python -m venv env
```

Activate it on Windows:

```bash
env\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Start XAMPP

Open **XAMPP Control Panel** and start:

- 🟢 Apache
- 🟢 MySQL

Open phpMyAdmin:

```text
http://localhost/phpmyadmin
```

### 5️⃣ Create the Database

Create a database named:

```text
food_express
```

Then import the project SQL dump.

### 6️⃣ Configure the Database

For local development:

```text
Host     : localhost
Port     : 3306
User     : root
Password : <your local MySQL password>
Database : food_express
```

For deployment, use environment variables instead of hard-coded credentials.

### 7️⃣ Run the Application

```bash
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

---

## 🗄️ Database

Food Express uses MySQL/MariaDB and includes tables for:

```text
👤 users
🏪 restaurants
📂 menu_categories
🍔 menu_items
🛒 cart
🛍️ cart_items
📦 orders
📋 order_items
💳 payments
🛵 delivery_persons
📍 delivery_assignments
📝 delivery_events
```

---

## ☁️ Deployment

Food Express can be deployed as a Flask application on **Render** using Gunicorn.

### ⚙️ Render Build Command

```bash
pip install -r requirements.txt
```

### ▶️ Render Start Command

```bash
gunicorn app:app
```

### 🔐 Environment Variables

Configure these variables in Render:

```text
MYSQL_HOST
MYSQL_PORT
MYSQL_USER
MYSQL_PASSWORD
MYSQL_DB
SECRET_KEY
```

### 🛢️ Cloud Database

The deployed application uses **Aiven MySQL** as the cloud database.

The database connection should use environment variables for the Aiven host, port, username, password, and database name.

🔒 Aiven MySQL may require SSL, so the production connection must be configured according to the Aiven service's SSL requirements.

---

## 🔒 Security

> ⚠️ **Important**

- 🔑 Never commit database passwords to GitHub.
- 🔐 Never commit production secret keys.
- 📄 Keep SQL dumps containing credentials private.
- 🌱 Use environment variables for production configuration.
- 🔒 Use properly hashed passwords for production authentication.
- 🚫 Never expose database credentials in screenshots or public repositories.

---

## 🐞 Troubleshooting

### ❌ `NameError: name 'render_template' is not defined`

Make sure `app.py` contains:

```python
from flask import Flask, render_template
```

### ❌ MySQL Connection Error

Check:

- ✅ Database service is running
- ✅ Host is correct
- ✅ Port is correct
- ✅ Username is correct
- ✅ Password is correct
- ✅ Database name is correct
- ✅ SSL configuration matches the cloud database

### ❌ Render Returns HTTP 500

Open the **Render application logs** and check the Python traceback.

The first application-level error in the traceback is usually the best place to start debugging.

---

## 📌 Project Status

🟢 **Active Development**

Food Express is a modular Flask food delivery application designed for local development with XAMPP and cloud deployment using Render + Aiven MySQL.

---

## 👨‍💻 Project

**Food Express — Group 09**

Built with ❤️ using **Python + Flask + MySQL**.

---

### ⭐ If you like this project

Give the repository a ⭐ and feel free to explore the code!
