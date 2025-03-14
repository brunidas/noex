import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager  # Cambié aquí de JWTExtended a JWTManager
from dotenv import load_dotenv 

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()  # Usa JWTManager en lugar de JWTExtended

def create_app():
    app = Flask(__name__)
    load_dotenv()
    app.config.from_prefixed_env()  # Lee variables de entorno con FLASK_*

    # Configuración de la base de datos
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
        f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
    )
    
    
    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)  # No cambies esto, sigue usando jwt.init_app(app)

    # Registrar blueprints
    from . import routes
    app.register_blueprint(routes.bp)

    return app
