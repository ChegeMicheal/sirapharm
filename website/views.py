from flask import Blueprint, render_template, flash, request, jsonify
from flask_login import  login_required, current_user
from . import db
from .models import User,Stock
import json
import mysql.connector

views = Blueprint('views',__name__)
host="localhost"
user="root"
passwd="MYSQLpassword2024"
database="user"

@views.route('/')
def homepage():
    #define getProductName method
    def getProductName():
        # Connect to the database
        mydb = mysql.connector.connect(
            host=host,
            user=user,
            passwd=passwd,
            database=database
            )

        mycursor = mydb.cursor()

        # Query the database with parameters as a tuple
        query = "SELECT productName FROM stock"
        mycursor.execute(query)

        # Fetch and print the results
        DBData = mycursor.fetchall()  # Use fetchone() for a single result
        print("Query:", query)
        print("DBData:", DBData)

        # Close the cursor and connection
        mycursor.close()
        mydb.close()

        return DBData
    return render_template('homepage.html', products=getProductName(), user=current_user)
