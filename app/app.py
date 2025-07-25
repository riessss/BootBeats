from flask import (
    Flask, 
    render_template
    )

def create_app():
    app = Flask(__name__)

    from sqlalchemy.orm import DeclarativeBase
    class Base(DeclarativeBase):
        pass
    
    from flask_sqlalchemy import SQLAlchemy
    db = SQLAlchemy(model_class=Base)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    db.init_app(app)

    from . import api
    app.register_blueprint(api.bp)

    @app.route('/')
    def index():
        return render_template('index.html')
    

    return app, db