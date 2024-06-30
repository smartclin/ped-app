from flask import Blueprint, request, jsonify
from datetime import datetime
from app import db
from app.models import Appointment, Doctor
from app.utils import response_json, token_required

appointments = Blueprint("appointments", __name__)


# Schedule Appointment
@appointments.route("/schedule", methods=["POST"])
@token_required
def schedule_appointment(current_user):
    data = request.get_json()

    if (
        not data
        or not data.get("doctor_id")
        or not data.get("appointment_date")
        or not data.get("reason")
    ):
        return response_json("Missing required fields", 400)

    doctor = Doctor.query.get(data["doctor_id"])

    if not doctor:
        return response_json("Doctor not found", 404)

    new_appointment = Appointment(
        patient_id=current_user.patient.id,
        doctor_id=data["doctor_id"],
        appointment_date=datetime.fromisoformat(data["appointment_date"]),
        reason=data["reason"],
        status="Pending",
    )

    db.session.add(new_appointment)
    db.session.commit()

    return response_json("Appointment scheduled successfully")


# Get Patient Appointments
@appointments.route("/patient", methods=["GET"])
@token_required
def get_patient_appointments(current_user):
    appointments = Appointment.query.filter_by(
        patient_id=current_user.patient.id).all()
    appointments_data = [
        {
            "id": appointment.id,
            "doctor": appointment.doctor.user.username,
            "appointment_date": appointment.appointment_date.isoformat(),
            "reason": appointment.reason,
            "status": appointment.status,
        }
        for appointment in appointments
    ]

    return jsonify(appointments_data)
