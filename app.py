from flask import Flask, jsonify,request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db_library.sqlite3'
app.config['SECRET_KEY'] = "random string"
db = SQLAlchemy(app)

# Create Student model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),  nullable=False)
    age = db.Column(db.Integer, nullable=False)

    def __init__(self,name,age):
        self.name=name
        self.age=age
    
    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'age': self.age}

# Get all students
@app.route('/students', methods=['GET'])
def get_all_students():
    students = Student.query.all()
    return jsonify([student.to_dict() for student in students])

# Get a student by id
@app.route('/student/<int:id>', methods=['GET'])
def get_student(id):
    student = Student.query.get(id)
    if student:
        return jsonify(student.to_dict())
    else:
        return jsonify({'error': 'student not found'}), 404

# Add a student
@app.route('/student/', methods=['POST'])
def add_student():
    name = request.json.get('name')
    age = request.json.get('age')
    if name and age:
        student = Student(name, age)
        db.session.add(student)
        db.session.commit()
        return jsonify({'message': 'student has been added'})
    else:
        return jsonify({'message': 'error'})

# Update a student by id
@app.route('/student/<int:id>', methods=['PUT'])
def update_student(id):
    student = Student.query.get(id)
    if student:
        name = request.json.get('name')
        age = request.json.get('age')
        if name:
            student.name = name
        if age:
            student.age = age
        db.session.commit()
        return jsonify(student.to_dict())
    else:
        return jsonify({'error': 'student not found'}), 404

# Delete a student by id
@app.route('/student/<int:id>', methods=['DELETE'])
def delete_student(id):
    student = Student.query.get(id)
    if student:
        # Delete the student from the session
        db.session.delete(student)
        # Commit the changes to the database
        db.session.commit()
        return jsonify({'message': 'student has been deleted'})
    else:
        return jsonify({'error': 'student not found'}), 404


if __name__ == '__main__':
    with app.app_context():
       db.create_all()
    app.run(debug=True)
