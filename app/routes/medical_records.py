from flask import Blueprint, request, jsonify
from datetime import datetime
from app import db
from app.models import MedicalRecord, Doctor
from app.utils import response_json, token_required

medical_records = Blueprint("medical_records", __name__)


# Create Medical Record
@medical_records.route("/create", methods=["POST"])
@token_required
def create_medical_record(current_user):
    data = request.get_json()

    if (
        not data
        or not data.get("doctor_id")
        or not data.get("diagnosis")
        or not data.get("notes")
    ):
        return response_json("Missing required fields", 400)

    doctor = Doctor.query.get(data["doctor_id"])

    if not doctor:
        return response_json("Doctor not found", 404)

    new_medical_record = MedicalRecord(
        patient_id=current_user.patient.id,
        doctor_id=data["doctor_id"],
        record_date=datetime.utcnow(),
        diagnosis=data["diagnosis"],
        notes=data["notes"],
    )

    db.session.add(new_medical_record)
    db.session.commit()

    return response_json("Medical record created successfully")


# Get Patient Medical Records
@medical_records.route("/patient", methods=["GET"])
@token_required
def get_patient_medical_records(current_user):
    medical_records = MedicalRecord.query.filter_by(
        patient_id=current_user.patient.id
    ).all()
    medical_records_data = [
        {
            "id": record.id,
            "doctor": record.doctor.user.username,
            "record_date": record.record_date.isoformat(),
            "diagnosis": record.diagnosis,
            "notes": record.notes,
        }
        for record in medical_records
    ]

    return jsonify(medical_records_data)
