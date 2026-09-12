import os
from flask import Flask
from flask_mysqldb import MySQL
from flask import Flask, render_template

mysql = MySQL()

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY", "local-dev-secret")

app.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST", "localhost")
app.config["MYSQL_PORT"] = int(os.environ.get("MYSQL_PORT", 3306))
app.config["MYSQL_USER"] = os.environ.get("MYSQL_USER", "root")
app.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD", "")
app.config["MYSQL_DB"] = os.environ.get("MYSQL_DB", "food_express")

mysql.init_app(app)





import admin_module.admin_routes as admin

import owner_module.app  as owner
import customer_module.app  as customer
import delivery_module.main as delivery

admin.register_routes(app,mysql)
customer.register_routes(app,mysql)
owner.register_routes(app,mysql)
delivery.register_routes(app,mysql)

@app.route('/')
def index():
    #return render_template('index.html')
    return render_template('index.html')


if __name__=='__main__':
    app.run(debug=True)
