from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime

    
class User(db.Model, UserMixin):
    id= db.Column(db.Integer, primary_key = True)
    fullName = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique = True, nullable=False)
    password = db.Column(db.String(1000))
    carts = db.relationship('Cart', backref='cart')
    

class Supplier(db.Model):
    id= db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    supplierName = db.Column(db.String(150), nullable=False)
    telephone = db.Column(db.String(100), nullable=False)
    date_submitted = db.Column(db.DateTime, default=datetime.utcnow)
    stocks = db.relationship('Stock', backref='supplier')
    supplies = db.relationship('Supply', backref='supply')
    
class Stock(db.Model):
    itemTally = db.Column(db.String(1000), nullable=False)
    productSellPrice = db.Column(db.Integer, nullable=False)
    id= db.Column(db.Integer, primary_key = True)
    productName = db.Column(db.String(150), nullable=False, unique=True)
    productBuyPrice = db.Column(db.Integer, nullable=False)
    buyPriceTally = db.Column(db.String(1000), nullable=False)
    stockQuantity= db.Column(db.Integer, nullable=False)
    ellPriceTally = db.Column(db.String(1000), nullable=False)
    expiryDate = db.Column(db.DateTime)
    supplierEmail = db.Column(db.String(150))
    imageFileName = db.Column(db.String(150))
    productCategory = db.Column(db.String(150))
    date_submitted = db.Column(db.DateTime, default=datetime.utcnow)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'))
    sales = db.relationship('Sale', backref='sales')
    

class Supply(db.Model):
    id= db.Column(db.Integer, primary_key = True)
    supplyProductName = db.Column(db.String(150), nullable=False)
    supplyProductBuyPrice = db.Column(db.Integer, nullable=False)
    supplyStockQuantity= db.Column(db.Integer, nullable=False)
    supplyExpiryDate = db.Column(db.DateTime, nullable=False)
    supplierEmail = db.Column(db.String(150), nullable=False)
    date_submitted = db.Column(db.DateTime, default=datetime.utcnow)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'))
    

class Sale(db.Model):
    id= db.Column(db.Integer, primary_key = True)
    saleProductName = db.Column(db.String(150), nullable=False)
    saleUnitPrice = db.Column(db.Integer, nullable=False)
    saleQuantity= db.Column(db.Integer, nullable=False)
    paymentMode = db.Column(db.String(150), nullable=False)
    customerName = db.Column(db.String(150), nullable=False)
    date_submitted = db.Column(db.DateTime, default=datetime.utcnow)
    stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'))
    
class SaleFetch(db.Model):
    id= db.Column(db.Integer, primary_key = True)
    saleProductName = db.Column(db.String(150), nullable=False)
    saleQuantity= db.Column(db.Integer, nullable=False)
    saleTally = db.Column(db.String(1000), nullable=False)
    date_submitted = db.Column(db.DateTime, default=datetime.utcnow)
    
class Cart(db.Model):
    id= db.Column(db.Integer, primary_key = True)
    productName = db.Column(db.String(150), nullable=False)
    imageFileName = db.Column(db.String(150))
    quantity= db.Column(db.Integer, nullable=False)    
    itemTally = db.Column(db.String(1000), nullable=False)
    paymentMode = db.Column(db.String(1000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    