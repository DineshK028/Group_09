from flask import Flask, render_template
from database import mysql


app = Flask(__name__)
app.secret_key = "secret key!!!!"
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'food_express'
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
