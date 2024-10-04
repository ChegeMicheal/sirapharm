from flask import Blueprint, Flask, render_template, request, flash, redirect, url_for
from .models import Supplier,User,Stock,Supply,Sale,SaleFetch,Cart,Order
import os
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import json
import mysql.connector
from random import randint

from flask_mysqldb import MySQL
import smtplib
from email.message import EmailMessage

auth = Blueprint('auth', __name__)

programDatabase = 1

if programDatabase == 1:
    host="localhost"
    user="root"
    passwd="hashimraj"
    database="user"
elif programDatabase == 2:
    host="mkorvuw3sl6cu9ms.cbetxkdyhwsb.us-east-1.rds.amazonaws.com"
    user="chmq59xthwhdmp9k"
    passwd="cicqmdv5hg2k41wz"
    database="qjtfk3q5n196eyyf"
elif programDatabase == 3:
    host="localhost"
    user="root"
    passwd="MYSQLpassword2024"
    database="user"


from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)

# Configure mail settings
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'terryrawlings50@gmail.com'  # Your email
app.config['MAIL_PASSWORD'] = 'wvqoffdittvrchet'  # Your app password or regular password
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

import logging

logging.basicConfig(level=logging.DEBUG)

@auth.route('/send_mail')
def send_mail():
    try:
        mail_message = Message(
            subject='Hello from Flask!',
            sender='chegemichael003@gmail.com',
            recipients=['hashimraj02@gmail.com']
        )
        mail_message.body = 'This is a test email.'
        mail.send(mail_message)
        return 'Mail sent!'
    except Exception as e:
        app.logger.error(f'Error: {e}')
        return f'An error occurred: {e}'
    

@auth.route("/sendEmail")
def send_email_to_multiple_recipients():
    # List of recipients
    recipients = ["hashimraj02@gmail.com", "terryrawlings50@gmail.com", "chegemichael003@gmail.com"]

    # Creating the message
    msg = Message("Email to Multiple Recipients",
                  sender="chegemichael003@gmail.com",
                  recipients=recipients)
    msg.body = "mzee, twende kwa johnte."

    
    # Sending the email
    mail.send(msg)
    
    return render_template('homepage.html')

@auth.route('/verifyEmail', methods=['GET', 'POST'])
def verifyEmail():
    if request.method == 'POST':
        email = request.form.get('email')
        
        def email_alert(subject, body, to):
            msg = EmailMessage()
            msg.set_content(body)
            msg['subject'] = subject
            msg['to'] = to
    
            user = "chegemichael@gmail.com"
            msg['from'] = user
            password=""
    
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.sratrttls()
            server.login(user, password)
            server.send_message(msg)
    
            server.quit()
            
        def codeGenerator():
            code = randint(100000,999999)
            return code
        
        code = codeGenerator()
        email_alert('EMAIL VERIFICATION CODE.', 'YOUR VERICATION CODE IS {{ code }}', email)#send email
        return code
    return render_template('verifyEmail.html', user=current_user)
    
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email = email).first()
        if user:
            if check_password_hash(user.password,password):
                flash('logged in successfully', category= 'success')
                login_user(user, remember=True)
                if user.id == 1:
                    return redirect(url_for('auth.admin'))
                else:
                    return redirect(url_for('auth.homepage'))
            else:
                flash('incorrect password, try again', category = 'error')
                
    
    return render_template("login.html", user = current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.dashboard'))

@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        fullName = request.form.get('fullname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('email already exists', category = 'error')
        elif len(email) < 4:
            flash('Email must be greater than 4 characters.', category='error')
        elif password1 != password2:
            flash('password mismatch', category='error')
        elif len(password1) < 7:
            flash('password must be atleast 7 characters.', category='error')
        else:
            #add user to database
            new_user = User(email = email, fullName=fullName, password = generate_password_hash(password1))
            db.session.add(new_user)
            db.session.commit()
            flash('account created successfully!', category='success')
            return redirect(url_for('auth.login'))
        
    return render_template("signUp.html", user = current_user)

@auth.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@auth.route('/supplier', methods=['GET', 'POST'])
def supplier():
    if request.method == 'POST':
        email = request.form.get('supplierEmail')
        supplierName = request.form.get('supplierName')
        telephone = request.form.get('supplierTelephone')
        #add supplier to database
        new_supplier = Supplier(email = email, supplierName=supplierName, telephone=telephone)
        db.session.add(new_supplier)
        db.session.commit()
        flash('supplier added successfully!', category='success')
        return render_template('dashboard.html')
    return render_template("supplier.html", user=current_user)
 
@auth.route('/supplierReport', methods=['GET', 'POST'])
@login_required
def supplierReport():       
    def getData():
        mydb = mysql.connector.connect(
            host=host,
            user=user,
            passwd=passwd,
            database=database
            )
        
        mycursor = mydb.cursor()

        mycursor.execute("SELECT * FROM supplier") 
        DBData = mycursor.fetchall() 
        print(DBData)
        mycursor.close()
        return DBData
         
    DBData = getData()
    return render_template("supplierReport.html", supplier=DBData, user=current_user)



@auth.route('/stock', methods=['GET', 'POST'])
@login_required
def stock():
    if request.method == 'POST':
        productName = request.form.get('productName')
        productCategory= request.form.get('productCategory')
        
        stockQuantity = 0
        productBuyPrice = 0
        productSellPrice = 0
        
        imageFileName = ''
        imageFileName = 'images/' + productName + '.png'
        itemTally=''
        buyPriceTally=''
        sellPriceTally=''
        
        for i in range(stockQuantity):
            itemTally+='|'
        
        for i in range(productBuyPrice):
            buyPriceTally+='|'
        
        for i in range(productSellPrice):
            sellPriceTally+='|'
               
        #add stock to database
        new_stock = Stock(productName=productName, itemTally=itemTally, stockQuantity=stockQuantity,productBuyPrice=productBuyPrice,productSellPrice=productSellPrice,buyPriceTally=buyPriceTally,sellPriceTally=sellPriceTally,imageFileName=imageFileName,productCategory=productCategory)
        db.session.add(new_stock)
        db.session.commit()
        flash('stock added successfully!', category='success')
        return render_template('dashboard.html', user=current_user)
    return render_template('stock.html', user=current_user)
   
@auth.route('/stockReport', methods=['GET', 'POST'])
@login_required
def stockReport():
    def getData():
        mydb = mysql.connector.connect(
            host=host,
            user=user,
            passwd=passwd,
            database=database
            )
        
        mycursor = mydb.cursor()

        mycursor.execute("SELECT id, productName, productBuyPrice, productSellPrice, stockQuantity, expiryDate, supplierEmail FROM stock") 
        DBData = mycursor.fetchall() 
        print(DBData)
        mycursor.close()
        return DBData
         
    DBData = getData()
    return render_template('stockReport.html', stock=DBData, user=current_user)


@auth.route('/supplyHistory', methods=['GET', 'POST'])
@login_required
def supplyHistory():
    if request.method == 'POST':
        supplyProductName = request.form.get('historyProduct')
        supplyProductBuyPrice = request.form.get('historyUnitPrice',type=int)
        proftMargin = request.form.get('profitMargin',type=int)
        supplyStockQuantity = request.form.get('historyQuantity', type=int)
        supplierEmail = request.form.get('historyEmail')
        supplyExpiryDate = request.form.get('historyExpiryDate')
        
        # Add supply to the database
        new_supply = Supply(
            supplyProductName=supplyProductName,
            supplyProductBuyPrice=supplyProductBuyPrice,
            supplyExpiryDate=supplyExpiryDate,
            supplyStockQuantity=supplyStockQuantity,
            supplierEmail=supplierEmail
        )
        db.session.add(new_supply)
        db.session.commit()
        
        if proftMargin < 20 and proftMargin > 100:
            profitMargin = proftMargin
        else:
            profitMargin = 20
        
        productSellPrice=int((supplyProductBuyPrice*(profitMargin/100)+supplyProductBuyPrice))
        supplyProdList = [supplyProductName]

        def getStockQuantity():
            # Connect to the database
            mydb = mysql.connector.connect(
                host=host,
                user=user,
                passwd=passwd,
                database=database
                )
    
            mycursor = mydb.cursor()
    
            # Query the database with parameters as a tuple
            query = "SELECT itemTally, stockQuantity, buyPriceTally, sellPriceTally  FROM stock WHERE productName=%s"
            mycursor.execute(query, (supplyProdList[0],))
    
            # Fetch and print the results
            DBData = mycursor.fetchall()
            print("Query:", query)
            print("Parameters:", (supplyProdList[0],))
            print("DBData:", DBData)
    
            # Close the cursor and connection
            mycursor.close()
            mydb.close()
    
            return DBData

        # Call the function
        stockQuantity = getStockQuantity()

        # Ensure there are results before trying to access them
        if stockQuantity:
            # Assuming you want the stockQuantity from the first result
            first_result = stockQuantity[0]
    
            # Check the length of the result tuple
            if len(first_result) > 1:
                oldStockQuantity = first_result[1]
                buyPrice=len(first_result[2])
                sellPrice=len(first_result[3])
                print(f"Old stock quantity: {oldStockQuantity}")
            else:
                print("Unexpected result format.")
        else:
            print("No data returned from the query.")
            oldStockQuantity = 0  # Default to 0 if no data

        # Calculate new stock quantity
        newStockQuantity = oldStockQuantity + supplyStockQuantity
        
        itemTally = ''
        for i in range(newStockQuantity):
            itemTally += '|'
            
        buyPriceTally = ''
        for i in range(supplyProductBuyPrice):
            buyPriceTally += '|'
            
        sellPriceTally = ''
        for i in range(productSellPrice):
            sellPriceTally += '|'
        
        def updateStock():
            # Connect to the database
            mydb = mysql.connector.connect(
                host=host,
                user=user,
                passwd=passwd,
                database=database
                )
            
            mycursor = mydb.cursor()
            
            # Correctly format the query with placeholders
            query = "UPDATE stock SET itemTally=%s, stockQuantity=%s, productBuyPrice=%s,productSellPrice=%s,expiryDate=%s,supplierEmail=%s, buyPriceTally=%s, sellPriceTally=%s WHERE productName=%s"
            mycursor.execute(query, (itemTally, newStockQuantity,supplyProductBuyPrice, productSellPrice, supplyExpiryDate, supplierEmail, buyPriceTally, sellPriceTally, supplyProdList[0]))
            
            mydb.commit()  # Don't forget to commit the changes
            mycursor.close()
            mydb.close()
        
        updateStock()
        flash('Stock added successfully!', category='success')
        return render_template('dashboard.html')
    return render_template('supplyHistory.html', user=current_user)

@auth.route('/supplyReport', methods=['GET', 'POST'])
@login_required
def supplyReport():    
    def getData():
        mydb = mysql.connector.connect(
            host=host,
            user=user,
            passwd=passwd,
            database=database
            )
        
        mycursor = mydb.cursor()

        mycursor.execute("SELECT id, supplyProductName, supplyProductBuyPrice, supplyStockQuantity, supplyExpiryDate, supplierEmail, date_submitted FROM supply") 
        DBData = mycursor.fetchall() 
        print(DBData)
        mycursor.close()
        return DBData
         
    DBData = getData()
    return render_template('supplyReport.html', supply=DBData, user=current_user)

@auth.route('/sales', methods=['GET', 'POST'])
@login_required
def sales():
    if request.method == 'POST':
        saleProductName = request.form.get('saleProductName')
        saleQuantity = request.form.get('saleQuantity', type=int)
        
        saleTally = ''
        for i in range(saleQuantity):
            saleTally += '|'
        
        # Add sale to the database
        new_confirmSale = SaleFetch(
            saleProductName=saleProductName,
            saleQuantity=saleQuantity,
            saleTally=saleTally
        )
        db.session.add(new_confirmSale)
        db.session.commit()
        return redirect(url_for('auth.confirmSale'))
    return render_template('sales.html', user=current_user)


@auth.route('/confirmSale', methods=['GET', 'POST'])
@login_required
def confirmSale():
    product_name = ''
    quantity = 0
    sellPrice = 0

    def getSale():
        # Connect to the database
        mydb = mysql.connector.connect(
            host=host,
            user=user,
            passwd=passwd,
            database=database
            )

        mycursor = mydb.cursor()

        # Query the database
        query = "SELECT saleProductName, saleTally FROM sale_fetch ORDER BY id DESC LIMIT 1;"
        mycursor.execute(query)

        # Fetch and print the results
        DBData = mycursor.fetchall()
        print("Query:", query)
        print("DBData:", DBData)

        # Close the cursor and connection
        mycursor.close()
        mydb.close()

        return DBData

    # Call the function
    sale = getSale()

    # Ensure there are results before trying to access them
    if sale:
        # Assuming you want the stockQuantity from the first result
        result = sale[0]

        # Check the length of the result tuple
        if len(result) > 1:
            product_name = result[0]
            quantity=len(result[1])
        else:
            print("Unexpected result format.")
    else:
        print("No data returned from the query.")
        
    # GET FORM DATA
    ProdList = [product_name]

    def getFormData():
        # Connect to the database
        mydb = mysql.connector.connect(
            host=host,
            user=user,
            passwd=passwd,
            database=database
            )

        mycursor = mydb.cursor()

        # Query the database
        query = "SELECT sellPriceTally FROM stock WHERE productName=%s"
        mycursor.execute(query, (ProdList[0],))

        # Fetch and print the results
        DBData = mycursor.fetchall()  
        print("Query:", query)
        print("DBData:", DBData)

        # Close the cursor and connection
        mycursor.close()
        mydb.close()

        return DBData

    # Call the function
    sellPriceTally = getFormData()

    # Ensure there are results before trying to access them
    if sellPriceTally:
        # Assuming you want the stockQuantity from the first result
        result = sellPriceTally[0]

        # Check the length of the result tuple
        if len(result) >= 1:
            sellPrice = len(result[0])
            print(sellPrice)
        else:
            print("Unexpected result format.")
    else:
        print("No data returned from the query.")
        
    if request.method == 'POST':
        # Extract form data
        saleProductName = request.form.get('saleProductName')
        saleUnitPrice = request.form.get('saleUnitPrice')
        saleQuantity = request.form.get('saleQuantity', type=int)
        customerName = request.form.get('customerName')
        paymentMode = request.form.get('paymentMode')
        saleItemsData = request.form.get('saleItemsData')

        # Process sale items from JSON
        try:
            saleItems = json.loads(saleItemsData)
        except json.JSONDecodeError:
            saleItems = []

        # Add sale to the database
        for item in saleItems:
            new_sale = Sale(
                saleProductName=item['product'],
                saleUnitPrice=item['unitPrice'],
                saleQuantity=item['quantity'],
                customerName=customerName,
                paymentMode=paymentMode
            )
            db.session.add(new_sale)
            db.session.commit()
        
        # Update stock table
        supplyProdList = [saleProductName]

        def getStockQuantity():
            # Connect to the database
            mydb = mysql.connector.connect(
                host=host,
                user=user,
                passwd=passwd,
                database=database
                )

            mycursor = mydb.cursor()

            # Query the database with parameters as a tuple
            query = "SELECT itemTally, stockQuantity FROM stock WHERE productName=%s"
            mycursor.execute(query, (supplyProdList[0],))

            # Fetch and print the results
            DBData = mycursor.fetchone()  # Use fetchone() for a single result
            print("Query:", query)
            print("Parameters:", (supplyProdList[0],))
            print("DBData:", DBData)

            # Close the cursor and connection
            mycursor.close()
            mydb.close()

            return DBData

        # Call the function
        stockQuantity = getStockQuantity()

        # Ensure there are results before trying to access them
        if stockQuantity:
            oldStockQuantity = stockQuantity[1]  # Extract old stock quantity
            print(f"Old stock quantity: {oldStockQuantity}")
        else:
            print("No data returned from the query.")
            oldStockQuantity = 0  # Default to 0 if no data

        # Calculate new stock quantity
        newStockQuantity = oldStockQuantity - saleQuantity
        
        # Create item tally string
        itemTally = '|' * newStockQuantity
        
        def updateStock():
            # Connect to the database
            mydb = mysql.connector.connect(
                host=host,
                user=user,
                passwd=passwd,
                database=database
                )

            mycursor = mydb.cursor()

            # Correctly format the query with placeholders
            query = "UPDATE stock SET itemTally=%s, stockQuantity=%s WHERE productName=%s"
            mycursor.execute(query, (itemTally, newStockQuantity, supplyProdList[0]))
            
            mydb.commit()  # Don't forget to commit the changes
            mycursor.close()
            mydb.close()
        
        updateStock()
        flash('Stock updated successfully!', category='success')
        return redirect(url_for('auth.confirmSale'))
     
    return render_template('confirmSale.html', product_name=product_name, sellPrice=sellPrice, quantity=quantity, user=current_user)
    
@auth.route('/salesReport', methods=['GET', 'POST'])
@login_required
def salesReport():        
    def getData():
        mydb = mysql.connector.connect(
            host=host,
            user=user,
            passwd=passwd,
            database=database
            )
        
        mycursor = mydb.cursor()
        mycursor.execute("SELECT id, saleProductName, saleUnitPrice, saleQuantity, customerName, paymentMode, date_submitted FROM sale") 
        DBData = mycursor.fetchall() 
        mycursor.close()
        return DBData
         
    DBData = getData()
    return render_template('salesReport.html', sales=DBData, user=current_user)



@auth.route('/homepage', methods=['GET', 'POST'])
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
    return render_template('homepage.html', products=getProductName(),  cart=ItemsIncart(),user=current_user)

app= Flask(__name__)
app.config["IMAGE_UPLOADS"]= r'C:\Users\ADMIN\Desktop\sirapharm\website\static\images'
app.config["ALLOWED_IMAGE_EXTENSIONS"]=["PNG","JPG","JPEG","GIF"]
app.config["MAX_IMAGE_FILESIZE"]=0.5 * 1024 * 1024

def allowed_image(filename):
    if not '.' in filename:
        return False
    
    ext = filename.rsplit('.',1)[1]

    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False
    
@auth.route('/upload_image', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        if request.files:
            
            image=request.files["image"]

            if image.filename == "":
                print("image must have a filename")
                return redirect(request.url)
            
            if not allowed_image(image.filename):
                print("that image extension is not allowed")
                return redirect(request.url)
            
            else:
                filename=secure_filename(image.filename)
                image.save(os.path.join(app.config["IMAGE_UPLOADS"],filename))
                flash('image uploaded successfully!')
                print("image saved!")
            
            return redirect(request.url)
    
            

    return render_template('upload_image.html', user=current_user)

@auth.route('/add2cart', methods=['GET', 'POST'])
@login_required
def add2cart():
    if request.method == 'POST':
        productName = request.form.get('productName')
        productPrice = request.form.get('productPrice',type=int)
        imageFileName = request.form.get('imageFileName')
        
        item = Cart.query.filter_by(productName=productName, status='cart', user_id=current_user.id).first()
        if item:
            flash('item already exists', category = 'error')
            return redirect(url_for('auth.cart'))
        else:
            quantity = 1
        
        
        
            itemTally=''
            priceTally=''
            user_id = current_user.id
            for i in range(quantity):
             itemTally+='|'
            for i in range(productPrice):
                 priceTally+='|'
            # Add cartItem to the database
            new_cart = Cart(
             productName=productName,
             productPrice=productPrice,
             priceTally=priceTally,
             imageFileName=imageFileName,
             quantity = quantity,
             itemTally=itemTally,
             status='cart',
             user_id = user_id
         )
            db.session.add(new_cart)
            db.session.commit()
        
            print(current_user)
                           
    return redirect(url_for('auth.homepage'))

@auth.route('/cart', methods=['GET', 'POST'])
@login_required
def cart():    
    return render_template('cartItems.html', cartItems=getCartItems(), cart=ItemsIncart(), totalPrice = cartTotal(), user=current_user)

@auth.route('/deleteCart', methods=['GET', 'POST'])
def deleteCart():
    if request.method == 'POST':
        id = request.form.get('product_id')
    
        list = [id]
        #define getProductName method
        def delCart():
            # Connect to the database
            mydb = mysql.connector.connect(
                host=host,
                user=user,
                passwd=passwd,
                database=database
                )

            mycursor = mydb.cursor()

            # Query the database with parameters as a tuple
            query = "DELETE FROM cart WHERE id=%s"
            mycursor.execute(query, (list[0],))
            
            mydb.commit()  # Don't forget to commit the changes
            
            print("Query:", query)
            print("Parameters:", (list[0],))

            # Close the cursor and connection
            mycursor.close()
            mydb.close()
    delCart()
    return redirect(url_for('auth.cart'))

@auth.route('/editCart', methods=['GET', 'POST'])
def editCart():
    if request.method == 'POST':
        id = request.form.get('product_id')
        name = request.form.get('productName')
        filename=request.form.get('imageFileName')
    return render_template('editCart.html', id=id, name=name,filename=filename, cart=ItemsIncart(), user=current_user)

@auth.route('/updateCart', methods=['GET', 'POST'])
def updateCart():
    if request.method == 'POST':
        id = request.form.get('product_id')
        quantitty = request.form.get('quantity',type=int)
        
        if quantitty > 1:
            quantity = quantitty
        else:
            quantity = 1
        
        itemTally = ''
        for i in range(quantity):
            itemTally+='|'
            
        list = [id]
        
        #define getProductName method
        def updateCart():
            # Connect to the database
            mydb = mysql.connector.connect(
                host=host,
                user=user,
                passwd=passwd,
                database=database
                )

            mycursor = mydb.cursor()

            # Correctly format the query with placeholders
            query = "UPDATE cart SET itemTally=%s, quantity=%s WHERE id=%s"
            mycursor.execute(query, (itemTally, quantity, list[0]))
            
            mydb.commit()  # Don't forget to commit the changes
            mycursor.close()
            mydb.close()
    updateCart()
    return redirect(url_for('auth.cart'))


import threading

def orderCart(order_num, cart_item_id):
    try:
        with mysql.connector.connect(
            host=host,
            user=user,
            passwd=passwd,
            database=database
        ) as mydb:
            with mydb.cursor() as mycursor:
                # Correctly format the query with placeholders
                query = "UPDATE cart SET status='order', orderNumber=%s WHERE id=%s"
                mycursor.execute(query, (order_num, cart_item_id))
            mydb.commit()  # Commit the changes
    except mysql.connector.Error as err:
        print(f"Error updating cart: {err}")

def updateCartItems(orderNum, cartItems):
    for item in cartItems:
        cart_item_id = item[3]  # Assuming item[3] contains the ID
        orderCart(orderNum, cart_item_id)  # Update the cart item status

@auth.route('/updateOrder', methods=['GET', 'POST'])
@login_required
def updateOrder():
    if request.method == 'POST':
        id = request.form.get('order_id')
        status = request.form.get('status')
        list = [id]
        
        #define getProductName method
        def update_order():
            # Connect to the database
            mydb = mysql.connector.connect(
                host=host,
                user=user,
                passwd=passwd,
                database=database
                )

            mycursor = mydb.cursor()

            # Correctly format the query with placeholders
            query = "UPDATE `order` SET status=%s WHERE id=%s"
            mycursor.execute(query, (status, list[0]))
            
            mydb.commit()  # Don't forget to commit the changes
            mycursor.close()
            mydb.close()
    update_order()
    return render_template('admin.html', orders=getAllOrders(), user=current_user)

@auth.route('/placeOrder', methods=['GET', 'POST'])
@login_required
def placeOrder():
    cartItems = getCartItems()
    orderNum = orderNumber() 
    ItemsCount = ItemsIncart()
    
    if request.method == 'POST':
        customerName = request.form.get('customerName')
        email = request.form.get('email')
        paymentMode = request.form.get('paymentMode')
        destination = request.form.get('destination')

        new_order = Order(
            ItemsCount=ItemsCount,
            destination=destination,
            customerName=customerName,
            paymentMode=paymentMode,
            email=email,
            status='pending',
            user_id=current_user.id
        )
        
        db.session.add(new_order)
        db.session.commit()

        # Start a new thread to update the cart items after response
        threading.Thread(target=updateCartItems, args=(orderNum, cartItems)).start()
        return redirect(url_for('auth.homepage'))

    # Handle GET request
    return render_template('placeOrder.html', totalPrice=cartTotal(), cartItems=getCartItems(), cart=0, user=current_user)

@auth.route('/orders', methods=['GET', 'POST'])
@login_required
def orders():
    
    return render_template('orders.html', orders=getOrders(), cart=ItemsIncart(), user=current_user)

@auth.route('/orderDetails', methods=['GET', 'POST'])
@login_required
def orderDetails():
    filename=''
    if request.method == 'POST':
        id = request.form.get('order_id')
        date_submitted = request.form.get('date_submitted')
        
        def getOrderItems():
            user_id = current_user.id
            list = [user_id]
            list1 = [id]
            # Connect to the database
            mydb = mysql.connector.connect(
                host=host,
                user=user,
                passwd=passwd,
                database=database
                )

            mycursor = mydb.cursor()

            # Query the database with parameters as a tuple
            query = "SELECT productName, quantity, itemTally, id, imageFileName, productPrice, priceTally FROM cart WHERE orderNumber=%s and user_id=%s"
            mycursor.execute(query, (list1[0],list[0]))

            # Fetch and print the results
            DBData = mycursor.fetchall()  # Use fetchone() for a single result
            print("Query:", query)
            print("DBData:", DBData)

            # Close the cursor and connection
            mycursor.close()
            mydb.close()

            return DBData
        
        orderDetails = getOrderItems()
        totalPrice = 0
        for i in range (len(orderDetails)):
            totalPrice = totalPrice + ((len(orderDetails[i][2]))*(len(orderDetails[i][6])))
      
    return render_template('orderDetails.html', orderDetails=orderDetails, filename=filename, order_id=id, date_submitted=date_submitted, totalPrice=totalPrice, cart=ItemsIncart(), user=current_user)


@auth.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if current_user.id != 1:
        return redirect(url_for('auth.homepage'))
    return render_template('admin.html', orders=getAllOrders(), user=current_user)

@auth.route('/orderFilter', methods=['GET', 'POST'])
@login_required
def orderFilter():
    if request.method == 'POST':
        status = request.form.get('status')
        
        def getFilteredOrders():
            list = [status]
            # Connect to the database
            mydb = mysql.connector.connect(
                host=host,
                user=user,
                passwd=passwd,
                database=database
                )

            mycursor = mydb.cursor()

            # Query the database with parameters as a tuple
            query = "SELECT customerName, email, ItemsCount, paymentMode, status, date_submitted,  id FROM `order` WHERE status=%s"
            mycursor.execute(query, (list[0],))

            # Fetch and print the results
            DBData = mycursor.fetchall()  # Use fetchone() for a single result
            print("Query:", query)
            print("Parameters:", (list[0],))
            ("DBData:", DBData)

            # Close the cursor and connection
            mycursor.close()
            mydb.close()

            return DBData
        orders = getFilteredOrders()
        return render_template('admin.html', orders=orders, user=current_user)

@auth.route('/adminOrderDetails', methods=['GET', 'POST'])
@login_required
def adminOrderDetails():
    filename=''
    if request.method == 'POST':
        id = request.form.get('order_id')
        date_submitted = request.form.get('date_submitted')
        
        def getOrderItems():
            list1 = [id]
            # Connect to the database
            mydb = mysql.connector.connect(
                host=host,
                user=user,
                passwd=passwd,
                database=database
                )

            mycursor = mydb.cursor()

            # Query the database with parameters as a tuple
            query = "SELECT productName, quantity, itemTally, id, imageFileName, productPrice, priceTally FROM cart WHERE orderNumber=%s"
            mycursor.execute(query, (list1[0],))

            # Fetch and print the results
            DBData = mycursor.fetchall()  # Use fetchone() for a single result
            print("Query:", query)
            print("DBData:", DBData)

            # Close the cursor and connection
            mycursor.close()
            mydb.close()

            return DBData
        
        orderDetails = getOrderItems()
        totalPrice = 0
        for i in range (len(orderDetails)):
            totalPrice = totalPrice + ((len(orderDetails[i][2]))*(len(orderDetails[i][6])))
      
    return render_template('adminOrderDetails.html', orderDetails=orderDetails, filename=filename, order_id=id, date_submitted=date_submitted, totalPrice=totalPrice, cart=ItemsIncart(), user=current_user)



def getCartItems():
    user_id = current_user.id
    list = [user_id]
    # Connect to the database
    mydb = mysql.connector.connect(
        host=host,
        user=user,
        passwd=passwd,
        database=database
        )

    mycursor = mydb.cursor()

    # Query the database with parameters as a tuple
    query = "SELECT productName, quantity, itemTally, id, imageFileName, productPrice, priceTally FROM cart WHERE user_id=%s and status='cart'"
    mycursor.execute(query, (list[0],))

    # Fetch and print the results
    DBData = mycursor.fetchall()  # Use fetchone() for a single result
    print("Query:", query)
    print("Parameters:", (list[0],))
    print("DBData:", DBData)

    # Close the cursor and connection
    mycursor.close()
    mydb.close()

    return DBData

def ItemsIncart():
    try:
        user_id = current_user.id
    except Exception as e:
        user_id = -1
    
    list = [user_id]
    
    def CartItems():
        # Connect to the database
        mydb = mysql.connector.connect(
            host=host,
            user=user,
            passwd=passwd,
            database=database
            )

        mycursor = mydb.cursor()

        # Query the database with parameters as a tuple
        query = "SELECT productName, itemTally FROM cart WHERE user_id=%s and status='cart'"
        mycursor.execute(query, (list[0],))

        # Fetch and print the results
        DBData = mycursor.fetchall()  # Use fetchone() for a single result
        print("Query:", query)
        print("Parameters:", (list[0],))
        print("DBData:", DBData)

        # Close the cursor and connection
        mycursor.close()
        mydb.close()

        return DBData
    
    cartItems = CartItems()
    cart = len(cartItems)
    return cart

def cartTotal():
    try:
        user_id = current_user.id
    except Exception as e:
        user_id = -1
    
    list = [user_id]
    
    def cartPrices():
        # Connect to the database
        mydb = mysql.connector.connect(
            host=host,
            user=user,
            passwd=passwd,
            database=database
            )

        mycursor = mydb.cursor()

        # Query the database with parameters as a tuple
        query = "SELECT priceTally, itemTally FROM cart WHERE user_id=%s and status='cart'"
        mycursor.execute(query, (list[0],))
        

        # Fetch and print the results
        DBData = mycursor.fetchall()  # Use fetchone() for a single result
        print("Query:", query)
        print("Parameters:", (list[0],))
        print("DBData:", DBData)

        # Close the cursor and connection
        mycursor.close()
        mydb.close()

        return DBData
    
    total = cartPrices()
    totalPrice = 0
    for i in range (len(total)):
        totalPrice = totalPrice + ((len(total[i][0]))*(len(total[i][1])))    
    return totalPrice

def orderNumber():
    list = ['try']
    def orders():
        # Connect to the database
        mydb = mysql.connector.connect(
            host=host,
            user=user,
            passwd=passwd,
            database=database
        )

        mycursor = mydb.cursor()

        # Query the database with parameters as a tuple
        mycursor.execute("SELECT id FROM `order`")

        # Fetch and print the results
        DBData = mycursor.fetchall()  # Use fetchone() for a single result
        print("DBData:", DBData)

        # Close the cursor and connection
        mycursor.close()
        mydb.close()

        return DBData
    
    orderNo = orders()
    orderNum = len(orderNo) + 1    
    
    return orderNum

def getOrders():
    user_id = current_user.id
    list = [user_id]
    # Connect to the database
    mydb = mysql.connector.connect(
        host=host,
        user=user,
        passwd=passwd,
        database=database
        )

    mycursor = mydb.cursor()

    # Query the database with parameters as a tuple
    query = "SELECT customerName, email, ItemsCount, paymentMode, status, date_submitted,  id FROM `order` WHERE user_id=%s"
    mycursor.execute(query, (list[0],))

    # Fetch and print the results
    DBData = mycursor.fetchall()  # Use fetchone() for a single result
    print("Query:", query)
    print("Parameters:", (list[0],))
    print("DBData:", DBData)

    # Close the cursor and connection
    mycursor.close()
    mydb.close()

    return DBData

def getAllOrders():
    # Connect to the database
    mydb = mysql.connector.connect(
        host=host,
        user=user,
        passwd=passwd,
        database=database
        )

    mycursor = mydb.cursor()

    # Query the database with parameters as a tuple
    query = "SELECT customerName, email, ItemsCount, paymentMode, status, date_submitted,  id FROM `order`"
    mycursor.execute(query)

    # Fetch and print the results
    DBData = mycursor.fetchall()  # Use fetchone() for a single result
    print("Query:", query)
    print("DBData:", DBData)

    # Close the cursor and connection
    mycursor.close()
    mydb.close()

    return DBData

@auth.route('/shop', methods=['GET', 'POST'])
def shop():
    if current_user != '':
        return redirect(url_for('auth.shopV'))
    else:
        return redirect(url_for('auth.userLogin'))

@auth.route('/shopV', methods=['GET', 'POST'])
def shopV():
    
    return render_template('homepage.html', user=current_user)

@auth.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        productName = request.form.get('products')
        # Update stock table
        searchProdList = [productName.lower()]
        searchPrdList = [productName]

        def getResults():
            # Connect to the database
            mydb = mysql.connector.connect(
                host=host,
                user=user,
                passwd=passwd,
                database=database
                )

            mycursor = mydb.cursor()

            # Query the database with parameters as a tuple
            query = "SELECT productName, productCategory, imageFileName, productSellPrice FROM stock WHERE productName=%s or productCategory=%s"
            mycursor.execute(query, (searchProdList[0],searchPrdList[0],))

            # Fetch and print the results
            DBData = mycursor.fetchall()  # Use fetchone() for a single result
            print("Query:", query)
            print("Parameters:", (searchProdList[0],))
            print("DBData:", DBData)

            # Close the cursor and connection
            mycursor.close()
            mydb.close()

            return DBData

        # Call the function
        search = getResults()
        filename=''
        
        if search:
            filename = search[0][2]   
            category = search[0][1] 
            
            rSearchProdList = [category]
            
            def getResult():
                # Connect to the database
                mydb = mysql.connector.connect(
                    host=host,
                    user=user,
                    passwd=passwd,
                    database=database
                    )

                mycursor = mydb.cursor()

                # Query the database with parameters as a tuple
                query = "SELECT productName, productCategory, imageFileName, productSellPrice FROM stock WHERE productCategory=%s"
                mycursor.execute(query, (rSearchProdList[0],))

                # Fetch and print the results
                DBData = mycursor.fetchall()  # Use fetchone() for a single result
                print("Query:", query)
                print("Parameters:", (rSearchProdList[0],))
                print("DBData:", DBData)

                # Close the cursor and connection
                mycursor.close()
                mydb.close()

                return DBData

            # Call the function
            relatedSearch = getResult()
        else:
            return redirect(url_for('auth.search404'))
        
    return render_template('search.html',search=search,relatedSearch=relatedSearch, filename=filename, user=current_user)

@auth.route('/search404', methods=['GET', 'POST'])
def search404():
    return render_template('search404.html', user=current_user)

#create custom error page(s)

#invalid url
@auth.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"),404

#internal server error
@auth.errorhandler(500)
def server_error(e):
    return render_template("500.html"),500