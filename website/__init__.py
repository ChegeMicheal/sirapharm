from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
app = Flask(__name__)
migrate=Migrate(app, db)
DB_NAME = 'users'


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'TRIAL KEY'

    #sqlite database
    #app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    #mysql
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:hashimraj@localhost/user'

    #mysql
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:MYSQLpassword2024@localhost/user'

    #jawsDB
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://chmq59xthwhdmp9k:cicqmdv5hg2k41wz@mkorvuw3sl6cu9ms.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/qjtfk3q5n196eyyf'

    #app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://u77ffnfeb72asn:pfa57c28b81fd1e85ee274336be11f7b0a49e63cb3d8e19d63a6763cf6f195e44@c5p86clmevrg5s.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d13aoi9fe4joeus'
    db.init_app(app)
    
    from .views import views
    from.auth import auth
    
    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/')
    
    from .models import User,Supplier,Stock,Supply,Sale,SaleFetch,Order
    
    create_database(app)
    
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
             db.create_all()
             print('database created!')
            
            #database_fatal_error ...(remove this after deployment)
            #db.drop_all()
            #print('database dropped!')

        