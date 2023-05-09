#app.py
from flask import Flask, jsonify, request
from flask_cors import CORS
from flaskext.mysql import MySQL #pip install flask-mysql
import pymysql
import mysql.connector as connection
import pandas as pd 
import json

## Data Processing

try:
    mydb = connection.connect(host="database-tp23.cbae3jtimquk.ap-southeast-2.rds.amazonaws.com", database = 'cv_db_7',user="admin", passwd="password",use_pure=True)
    query = "SELECT * FROM `Co2_per_states`"
    data = pd.read_sql(query,mydb)
    mydb.close() #close the connection
except Exception as e:
    mydb.close()
    print(str(e))

with open('states.min.geojson', 'r') as f:
    data1 = json.load(f)

data2 = data[data.year == 2000].reset_index(drop= True).round(2)

for i in range(len(data1["features"])):
    print(data1["features"][i]["properties"]["STATE_NAME"])
    
    data1["features"][i]["properties"]["name"] = data2["state"][i]
    data1["features"][i]["properties"]["density"] = data2["net_co2"][i]

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
    cur.execute("SELECT Make, Model, `Vehicle Class`, ROUND(AVG(`CO2 Emissions(g/km)`),1) AS CO2 FROM `co2_emissions_australia` group by Make, Model, `Vehicle Class`")
    data = cur.fetchall()
    cur.close()
    return jsonify(data)

@app.route("/mysql1")
def get_mysql_data1():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT Make, ROUND(AVG(`CO2 Emissions(g/km)`)) AS CO2 FROM `co2_emissions_australia` group by Make")
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
    cur.execute(f"SELECT Model, `Vehicle Class`, ROUND(AVG(`CO2 Emissions(g/km)`),1) AS CO2 FROM `co2_emissions_australia` WHERE Make = '{string_get}' group by Model, `Vehicle Class`")
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
    cur.execute(f"SELECT ROUND(AVG(`CO2 Emissions(g/km)`),1) AS CO2 FROM `co2_emissions_australia` WHERE Make = '{string_get}'")
    data = cur.fetchall()
    cur.close()
    return jsonify(data)

@app.route("/search1")
def render_data():
    string = request.args

    string_get = string.get("message")
    
    print(string.get("message"))
    
    data2 = data[data.year == int(string_get)].reset_index(drop= True).round(2)
    
    for i in range(len(data1["features"])):
    
        data1["features"][i]["properties"]["name"] = data2["state"][i]
        data1["features"][i]["properties"]["density"] = data2["net_co2"][i]
    
    return data1

@app.route('/receive_state', methods=['GET'])
def receive_string_data():
    string = request.args

    string_get = string.get("message")
    # do something with the string
    print(string.get("message"))
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute(f"SELECT `net_co2` AS co2 FROM `Co2_per_states` WHERE state = '{string_get}' ORDER BY year")
    data = cur.fetchall()
    
    for i in range(len(data)):
        data[i]['co2'] = float(data[i]['co2'])
        
    cur.close()
    return jsonify(data)

@app.route("/get_fulldata")
def get_mysql_data2():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute(f"SELECT `net_co2` AS co2, state, year FROM `Co2_per_states`")
    data = cur.fetchall()
    cur.close()
    return jsonify(data)

@app.route("/get_fulldata1")
def get_mysql_data3():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute(f"SELECT * FROM `Co2_per_states`")
    data = cur.fetchall()
    cur.close()
    return jsonify(data)

if __name__ == '__main__':
    app.run(host="0.0.0.0")
