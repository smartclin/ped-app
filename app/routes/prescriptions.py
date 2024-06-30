from flask import Blueprint, request, jsonify
from app import db
from app.models import Prescription, Patient, Doctor
from app.utils import response_json, token_required

prescriptions = Blueprint("prescriptions", __name__)


# Create Prescription
@prescriptions.route("/create", methods=["POST"])
@token_required
def create_prescription(current_user):
    data = request.get_json()

    if (
        not data
        or not data.get("doctor_id")
        or not data.get("patient_id")
        or not data.get("medications")
    ):
        return response_json("Missing required fields", 400)

    doctor = Doctor.query.get(data["doctor_id"])
    patient = Patient.query.get(data["patient_id"])

    if not doctor or not patient:
        return response_json("Doctor or patient not found", 404)

    new_prescription = Prescription(
        doctor_id=data["doctor_id"],
        patient_id=data["patient_id"],
        medications=data["medications"],
    )

    db.session.add(new_prescription)
    db.session.commit()

    return response_json("Prescription created successfully")


# Get Patient Prescriptions
@prescriptions.route("/patient", methods=["GET"])
@token_required
def get_patient_prescriptions(current_user):
    prescriptions = Prescription.query.filter_by(
        patient_id=current_user.patient.id
    ).all()
    prescriptions_data = [
        {
            "id": prescription.id,
            "doctor": prescription.doctor.user.username,
            "medications": prescription.medications,
            "created_at": prescription.created_at.isoformat(),
        }
        for prescription in prescriptions
    ]

    return jsonify(prescriptions_data)
