from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask import render_template
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "saas_growth.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'  # Change this in production
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize SQLAlchemy with the app
    db.init_app(app)
    
    # Initialize Login Manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        from .models.user import User
        return User.query.get(int(id))

    # Register blueprints
    from .routes.auth import auth
    from .routes.main import main
    from .routes.analytics import analytics

    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(main, url_prefix='/')
    app.register_blueprint(analytics, url_prefix='/analytics')

    # Create database tables
    from .models.user import User
    from .models.metrics import Metrics

    # Ensure the instance folder exists
    if not os.path.exists('instance'):
        os.makedirs('instance')

    # Create all database tables
    with app.app_context():
        db.drop_all()  # Drop all existing tables
        db.create_all()  # Create new tables with updated schema

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    return app