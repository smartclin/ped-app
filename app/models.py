from app import db  # Assuming `db` is the SQLAlchemy instance


# User Model (Basic User Information)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f"<User {self.username}>"


# Doctor Model
class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", backref=db.backref("doctor", uselist=False))
    speciality = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.Text)
    image_url = db.Column(db.String(255))

    def __repr__(self):
        return f"<Doctor {self.user.username}>"


# Patient Model
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User",
                           backref=db.backref("patient",
                                              uselist=False))
    birth_date = db.Column(db.Date)
    gender = db.Column(db.String(10))
    address = db.Column(db.String(255))
    phone_number = db.Column(db.String(20))

    def __repr__(self):
        return f"<Patient {self.user.username}>"


# Appointment Model
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer,
                           db.ForeignKey("patient.id"),
                           nullable=False)
    patient = db.relationship(
        "Patient", backref=db.backref("appointments", lazy="dynamic")
    )
    doctor_id = db.Column(db.Integer,
                          db.ForeignKey("doctor.id"),
                          nullable=False)
    doctor = db.relationship(
        "Doctor", backref=db.backref("appointments", lazy="dynamic")
    )
    appointment_date = db.Column(db.DateTime)
    reason = db.Column(db.Text)
    status = db.Column(db.String(50))  # Pending, Confirmed, Cancelled

    def __repr__(self):
        return f"<Appointment {self.id}>"


# Medical Record Model
class MedicalRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer,
                           db.ForeignKey("patient.id"),
                           nullable=False)
    patient = db.relationship(
        "Patient", backref=db.backref("medical_records", lazy="dynamic")
    )
    doctor_id = db.Column(db.Integer,
                          db.ForeignKey("doctor.id"),
                          nullable=False)
    doctor = db.relationship(
        "Doctor", backref=db.backref("medical_records", lazy="dynamic")
    )
    record_date = db.Column(db.DateTime)
    diagnosis = db.Column(db.Text)
    notes = db.Column(db.Text)

    def __repr__(self):
        return f"<MedicalRecord {self.id}>"


# Prescription Model
class Prescription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    medical_record_id = db.Column(
        db.Integer, db.ForeignKey("medical_record.id"), nullable=False
    )
    medical_record = db.relationship(
        "MedicalRecord", backref=db.backref("prescriptions", lazy="dynamic")
    )
    medication = db.Column(db.String(255))
    dosage = db.Column(db.String(50))
    instructions = db.Column(db.Text)

    def __repr__(self):
        return f"<Prescription {self.id}>"


# Medical Center Model
class MedicalCenter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255))
    phone_number = db.Column(db.String(20))
    email = db.Column(db.String(120))
    website = db.Column(db.String(255))
    image_url = db.Column(db.String(255))

    def __repr__(self):
        return f"<MedicalCenter {self.name}>"


# Health Tip Model
class HealthTip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<HealthTip {self.title}>"


# Payment Model
class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(
        db.Integer, db.ForeignKey("appointment.id"), nullable=False
    )
    appointment = db.relationship(
        "Appointment", backref=db.backref("payments", lazy="dynamic")
    )
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    status = db.Column(db.String(50))  # Paid, Refunded

    def __repr__(self):
        return f"<Payment {self.id}>"
