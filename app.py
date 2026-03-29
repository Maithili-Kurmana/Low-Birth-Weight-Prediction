import numpy as np
import pandas as pd
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb

from flask import Flask, request, render_template
import joblib

# Load ML Model
model = joblib.load('final_pickle_model.pk1')

app = Flask(__name__)

# Database Connection
db = MySQLdb.connect(
    host="localhost",
    user="root",
    passwd="",
    db="ddbbb",
    port=3307
)

cursor = db.cursor()

gmail_list = []
password_list = []
gmail_list1 = []

# Home Page
@app.route('/')
def home():
    return render_template('register.html')


# Register
@app.route('/register', methods=['POST'])
def register():

    data = [str(x) for x in request.form.values()]
    username = data[0]
    password = data[1]

    db = MySQLdb.connect(
    host="localhost",
    user="root",
    passwd="",
    db="ddbbb",
    port=3307
)
    cursor = db.cursor()

    cursor.execute("SELECT user FROM user_register")
    result = cursor.fetchall()

    gmail_list1.clear()

    for row in result:
        gmail_list1.append(str(row[0]))

    if username in gmail_list1:
        return render_template('register.html', text="Username already exists")

    else:
        sql = "INSERT INTO user_register(user,password) VALUES (%s,%s)"
        val = (username, password)

        cursor.execute(sql, val)
        db.commit()
        db.close()

        return render_template('register.html', text="Successfully Registered")


# Login Page
@app.route('/login')
def login():
    return render_template('login.html')


# Login Check
@app.route('/logedin', methods=['POST'])
def logedin():

    data = [str(x) for x in request.form.values()]
    username = data[0]
    password = data[1]

    db = MySQLdb.connect(
    host="localhost",
    user="root",
    passwd="",
    db="ddbbb",
    port=3307
)
    cursor = db.cursor()

    cursor.execute("SELECT user,password FROM user_register")
    result = cursor.fetchall()

    gmail_list.clear()
    password_list.clear()

    for row in result:
        gmail_list.append(str(row[0]))
        password_list.append(str(row[1]))

    if username in gmail_list and password_list[gmail_list.index(username)] == password:
        return render_template('index1.html')
    else:
        return render_template('login.html', text="Invalid Username or Password")


# Prediction Page
@app.route('/production')
def production():
    return render_template('index1.html')


# Prediction
@app.route('/production/predict', methods=['POST'])
def predict():

    values = [float(x) for x in request.form.values()]

    data = {
        'MAGE':[values[0]],
        'FAGE':[values[1]],
        'GAINED':[values[2]],
        'VISITS':[values[3]],
        'TOTALP':[values[4]],
        'BDEAD':[values[5]],
        'TERMS':[values[6]],
        'LOUTCOME':[values[7]],
        'WEEKS':[values[8]],
        'CIGNUM':[values[9]],
        'DRINKNUM':[values[10]],
        'UTERINE':[values[11]]
    }

    df = pd.DataFrame(data)

    prediction = model.predict(df)

    weight_pound = float(prediction[0])
    weight_grams = weight_pound * 453.592
    weight_kg = weight_grams / 1000

    if weight_kg < 2.5:
        category = "Low Birth Weight"
    elif weight_kg < 4.5:
        category = "Normal Birth Weight"
    else:
        category = "Abnormal Birth Weight"

    return render_template(
        'index1.html',
        prediction_text="Fetal Birth Weight is {:.2f} kg".format(weight_kg),
        prediction_text1=category
    )


if __name__ == "__main__":
    app.run(debug=True)