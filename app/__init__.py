from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask import redirect, url_for, session
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail


from datetime import datetime
#from app.models import Task, User 
from flask import current_app

#create database object globally
db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


    
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'your_email@gmail.com'       
    app.config['MAIL_PASSWORD'] = 'your_app_password'          
    app.config['MAIL_DEFAULT_SENDER'] = 'your_email@gmail.com'

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)

  


    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'


    from app.routes.auth import auth_bp
    from app.routes.tasks import tasks_bp

    from app.routes.home import home_bp
    from app.routes.reminders import reminders_bp, start_scheduler
    
    


    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(tasks_bp, url_prefix="/tasks")

    app.register_blueprint(home_bp)
    app.register_blueprint(reminders_bp)
    
    
    
    start_scheduler(app)


    @app.route('/')
    def home():
        if 'user_id' in session:
            return redirect(url_for('tasks.view_tasks'))
        else:
            return redirect(url_for('auth.login'))

    

    with app.app_context():
        from app import models
        db.create_all()

    return app

