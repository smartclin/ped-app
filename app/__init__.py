# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_filename=None):
    app = Flask(__name__)

    if config_filename:
        app.config.from_pyfile(config_filename)
    else:
        app.config.from_pyfile("config.py")

    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    with app.app_context():
        # Import blueprints
        from app.routes.auth import auth
        from app.routes.users import users
        from app.routes.appointments import appointments
        from app.routes.medical_records import medical_records
        from app.routes.prescriptions import prescriptions
        from app.routes.payments import payments
        from app.routes.health_tips import health_tips

        # Register blueprints
        app.register_blueprint(auth, url_prefix="/auth")
        app.register_blueprint(users, url_prefix="/users")
        app.register_blueprint(appointments, url_prefix="/appointments")
        app.register_blueprint(medical_records, url_prefix="/medical_records")
        app.register_blueprint(prescriptions, url_prefix="/prescriptions")
        app.register_blueprint(payments, url_prefix="/payments")
        app.register_blueprint(health_tips, url_prefix="/health_tips")

        # Import models to ensure they are registered with SQLAlchemy
        from app.models import (
            User,
            Doctor,
            Patient,
            Appointment,
            MedicalRecord,
            Prescription,
        )

    @app.route("/")
    def index():
        return "Welcome to the Medical Services API"

    @app.shell_context_processor
    def make_shell_context():
        return {
            "db": db,
            "User": User,
            "Doctor": Doctor,
            "Patient": Patient,
            "Appointment": Appointment,
            "MedicalRecord": MedicalRecord,
            "Prescription": Prescription,
        }

    return app
