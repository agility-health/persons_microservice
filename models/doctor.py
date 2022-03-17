from config import db

doctor_education = db.Table('doctor_education', db.metadata,
                      db.Column('doctor_id', db.Integer, db.ForeignKey('doctor.id')),
                      db.Column('education_id', db.Integer, db.ForeignKey('education.id'))
                      )


class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(32))
    surname = db.Column(db.String(32), index=True)
    birthday = db.Column(db.Date)
    education = db.relationship('Education', secondary=doctor_education, backref= db.backref('doctor', lazy=True))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", back_populates="doctor", uselist=False)

class Education(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    university_name = db.Column(db.String(64))
    specialization = db.Column(db.String(64))
    education_degree = db.Column(db.String(64))
    date_of_graduation = db.Column(db.Date)
