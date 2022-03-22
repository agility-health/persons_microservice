from models.doctor import Doctor


def get_doctor_by_id(doctor_id):
    return Doctor.query.filter_by(id=doctor_id).first()


def get_education_by_id_from_doctor(doctor, education_id):
    education_list = [education for education in doctor.education if education.id == int(education_id)]
    if education_list:
        return education_list[0]
    return None