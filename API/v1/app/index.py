import os
from flask import Flask
from flask_cors import CORS
from flask_pymongo import PyMongo
from dotenv import load_dotenv
 
# Carga las variables del .env
load_dotenv()
 
mongo = PyMongo()
 
def create_app():
    app = Flask(__name__)
   
    # Usa la variable del entorno en lugar de hardcodear la URI
    app.config["MONGO_URI"] = os.getenv("MONGO_URI")
 
    mongo.init_app(app)
   
    CORS(app, origins="*")
 
    from .controladores.prendas import prendas_endpoints
    app.register_blueprint(prendas_endpoints, url_prefix="/admin2/api/v1")

    from .controladores.usuarios import usuarios_endpoints
    app.register_blueprint(usuarios_endpoints, url_prefix="/admin2/api/v1")

    from .controladores.ventas import ventas_endpoints
    app.register_blueprint(ventas_endpoints, url_prefix="/admin2/api/v1")

    from .controladores.reportes import reportes_endpoints
    app.register_blueprint(reportes_endpoints, url_prefix="/admin2/api/v1")

    
 
    return app
 