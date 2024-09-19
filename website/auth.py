from flask import Blueprint, Flask, render_template, request, flash, redirect, url_for
from .models import Supplier,User,Stock,Supply,Sale,SaleFetch
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
host="localhost"
user="root"
passwd="hashimraj"
database="user"

#host="mkorvuw3sl6cu9ms.cbetxkdyhwsb.us-east-1.rds.amazonaws.com"
#user="ujwh39au1e2iiwzc"
#passwd="ooxt9nik14itgjvs"
#database="ta87as92i9tzhnji"
host="mkorvuw3sl6cu9ms.cbetxkdyhwsb.us-east-1.rds.amazonaws.com"
user="ujwh39au1e2iiwzc"
passwd="ooxt9nik14itgjvs"
database="ta87as92i9tzhnji"


from flask_mail import Mail, Message

app = Flask(__name__)

app.config['MAIL_SERVER']= 'live.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'chegemichael003@gmail.com'
app.config['MAIL_PASSWORD'] = 'Mbogo5836'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

@app.route("/sendEmail")
def send_email_to_multiple_recipients():
    # List of recipients
    recipients = ["hashimraj02@gmail.com", "terryrawlings50@gmail.com"]

    # Creating the message
    msg = Message("Email to Multiple Recipients",
                  sender="chegemichael003@gmail.com",
                  recipients=recipients)
    msg.body = "mzee, twende kwa johnte."

    
    # Sending the email
    mail.send(msg)
    
    return "Email sent to multiple recipients!"

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
                return redirect(url_for('auth.dashboard'))
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
        stockQuantity = 0
        productBuyPrice = 0
        productSellPrice = 0
        
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
        new_stock = Stock(productName=productName, itemTally=itemTally, stockQuantity=stockQuantity,productBuyPrice=productBuyPrice,productSellPrice=productSellPrice,buyPriceTally=buyPriceTally,sellPriceTally=sellPriceTally)
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
    return render_template('homepage.html', products=getProductName(), user=current_user)

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
    



@auth.route('/datalist', methods=['GET', 'POST'])
def datalist():
  return render_template('datalist.html')  


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


@auth.route('/send_messages', methods=['GET', 'POST'])
def send_messages():
    if request.method == 'POST':
        email = request.form.get('email')
        message = request.form.get('message')
        visibility = request.form.get('visibility')
        #add user to database
        new_message = User(email = email, message=message, visibility=visibility)
        db.session.add(new_message)
        db.session.commit()
        flash('message submitted!', category='success')
        
    return render_template("homepage.html")
    


@auth.route('/view_messages', methods=['GET', 'POST'])
def view_messages():
    
    def getData():
        mydb = mysql.connector.connect(
             host="d1kb8x1fu8rhcnej.cbetxkdyhwsb.us-east-1.rds.amazonaws.com",
             user="mgewt9r4y3xqrzx9",
             passwd="tic4d2e6fe79vw98",
             database="c60lhk7e30osyo5v"
            )
        
        mycursor = mydb.cursor()

        mycursor.execute("SELECT * FROM footer_message WHERE visibility='public'") 
        DBData = mycursor.fetchall() 
        print(DBData)
        mycursor.close()
        return DBData
         
    DBData = getData()
    return render_template("messages.html", footer_message=DBData)

@auth.route('/view_private_messages', methods=['GET', 'POST'])
def view_private_messages():
    
    def getData():
        mydb = mysql.connector.connect(
             host="d1kb8x1fu8rhcnej.cbetxkdyhwsb.us-east-1.rds.amazonaws.com",
             user="mgewt9r4y3xqrzx9",
             passwd="tic4d2e6fe79vw98",
             database="c60lhk7e30osyo5v"
            )
        
        mycursor = mydb.cursor()

        mycursor.execute("SELECT * FROM footer_message WHERE visibility='private'") 
        DBData = mycursor.fetchall() 
        print(DBData)
        mycursor.close()
        return DBData
         
    DBData = getData()
    return render_template("private_messages.html", footer_message=DBData)

    #footer_message = Footer_message.query.all()
    #print(footer_message)
    #return render_template('messages.html', footer_message=footer_message)


#create custom error pages

#invalid url
@auth.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"),404

#internal server error
@auth.errorhandler(500)
def server_error(e):
    return render_template("500.html"),500

