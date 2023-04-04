#app.py
from flask import Flask, jsonify, request
from flask_cors import CORS
from flaskext.mysql import MySQL #pip install flask-mysql
import pymysql

# configuration
DEBUG = True
 
# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)
     
mysql = MySQL()
    
app.config['MYSQL_DATABASE_USER'] = 'admin'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'cv_db_7'
app.config['MYSQL_DATABASE_HOST'] = 'database-tp23.cbae3jtimquk.ap-southeast-2.rds.amazonaws.com'
mysql.init_app(app)
 
# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

@app.route("/mysql")
def get_mysql_data():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT Make, Model, `Vehicle Class`, ROUND(AVG(`CO2 Emissions(g/km)`),1) AS CO2 FROM `co2_emissions_canada` group by Make, Model, `Vehicle Class`")
    data = cur.fetchall()
    cur.close()
    return jsonify(data)

@app.route("/mysql1")
def get_mysql_data1():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT Make, ROUND(AVG(`CO2 Emissions(g/km)`)) AS CO2 FROM `co2_emissions_canada` group by Make")
    data = cur.fetchall()
    cur.close()
    return jsonify(data)

@app.route('/search', methods=['GET'])
def receive_string():
    string = request.args

    string_get = string.get("message")
    # do something with the string
    print(string.get("message"))
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute(f"SELECT Model, `Vehicle Class`, ROUND(AVG(`CO2 Emissions(g/km)`),1) AS CO2 FROM `co2_emissions_canada` WHERE Make = '{string_get}' group by Model, `Vehicle Class`")
    data = cur.fetchall()
    cur.close()
    return jsonify(data)

@app.route('/carbon', methods=['GET'])
def receive_string2():
    string = request.args

    string_get = string.get("message")
    # do something with the string
    print(string.get("message"))
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute(f"SELECT ROUND(AVG(`CO2 Emissions(g/km)`),1) AS CO2 FROM `co2_emissions_canada` WHERE Make = '{string_get}'")
    data = cur.fetchall()
    cur.close()
    return jsonify(data)

if __name__ == '__main__':
    app.run()