from service import db


class Application(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    animal = db.Column(db.String(length=30),nullable=False)
    color = db.Column(db.String())
    tail = db.Column(db.String())
    photo = db.Column(db.Integer(), db.ForeignKey('photos.id'))
    status = db.Column(db.Boolean(), default=False)


class Photos(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    id_application = db.Column(db.Integer(),nullable=True)
    filename = db.Column(db.String(), nullable=True)
    is_animal_there = db.Column(db.Integer(), nullable=True)
    is_it_a_dog = db.Column(db.Integer(), nullable=True)
    is_the_owner = db.Column(db.Integer(), nullable=True)
    color = db.Column(db.String(), nullable=True)
    tail = db.Column(db.String(), nullable=True)
    address = db.Column(db.String(), nullable=True)
    cam_id = db.Column(db.String(), nullable=True)
    result = db.Column(db.Boolean, nullable=True)


    def __repr__(self):
        return (self.id_application, self.filename, self.is_animal_there, self.is_it_a_dog, self.is_the_owner, self.color, self.tail, self.address, self.cam_id)




# db.create_all()