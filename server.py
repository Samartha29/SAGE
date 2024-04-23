from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  # Import the CORS extension
import hashlib
from datetime import datetime
import os
from model_trainer import get_recommendations

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'  # Change this to a secure random key

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(100), nullable=False)
    
class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    score = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Check if the users table exists
if not os.path.exists('user_database.db'):
    with app.app_context():
        db.create_all()

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'user': {'id': new_user.id, 'username': new_user.username}})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    user = User.query.filter_by(username=username, password=hashed_password).first()

    if user:
        session['user_id_' + str(user.id)] = True
        return jsonify({'user': {'id': user.id, 'username': user.username}})
    else:
        return jsonify({'error': 'Invalid username or password'}), 401

@app.route('/logout')
def logout():
    user_id = session.get('user_id')
    if user_id:
        session.pop('user_id_' + str(user_id), None)
        return jsonify({'message': 'Logged out successfully'})
    else:
        return jsonify({'message': 'No user logged in'})
    
@app.route('/create_course', methods=['POST'])
def create_course():
    data = request.get_json()
    course_name = data.get('course_name')

    if not course_name:
        return jsonify({'error': 'Course name is required'}), 400

    new_course = Course(course_name=course_name)
    db.session.add(new_course)
    db.session.commit()

    return jsonify({'course': {'id': new_course.id, 'course_name': new_course.course_name}})

@app.route('/delete_course/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    course = Course.query.get(course_id)

    if not course:
        return jsonify({'error': 'Course not found'}), 404

    db.session.delete(course)
    db.session.commit()

    return jsonify({'message': 'Course deleted successfully'})

@app.route('/get_all_courses', methods=['GET'])
def get_all_courses():
    courses = Course.query.all()

    course_list = [{'id': course.id, 'course_name': course.course_name} for course in courses]

    return jsonify({'courses': course_list})
    
@app.route('/submit_test', methods=['POST'])
def submit_test():
    data = request.get_json()
    user_id = data.get('user_id')
    course_id = data.get('course_id')
    score = data.get('score')

    if not user_id or not course_id or not score:
        return jsonify({'error': 'User ID, Course ID, and Score are required'}), 400

    new_test = Test(user_id=user_id, course_id=course_id, score=score)
    db.session.add(new_test)
    db.session.commit()

    return jsonify({'test': {'id': new_test.id, 'user_id': new_test.user_id, 'course_id': new_test.course_id, 'score': new_test.score, 'timestamp': new_test.timestamp}})

@app.route('/get_test_scores/<int:user_id>/<int:course_id>', methods=['GET'])
def get_test_scores(user_id, course_id):
    tests = Test.query.filter_by(user_id=user_id, course_id=course_id).order_by(Test.timestamp.asc()).all()

    test_list = [
        {
            'id': test.id,
            'score': test.score,
            'timestamp': test.timestamp.isoformat()  # Convert to ISO format for better readability
        }
        for test in tests
    ]

    return jsonify({'test_scores': test_list})

@app.route('/recommend', methods=['POST'])    
def recommend():
    data = request.get_json()
    prompt = data.get('prompt')
    advanced = data.get('advanced', False)

    recommendations = get_recommendations(prompt, advanced)

    return jsonify({'courses': recommendations}), 200

@app.route('/average_scores/<int:course_id>', methods=['GET'])
def average_scores(course_id):
    # Use SQL to calculate average scores and retrieve usernames
    result = db.session.query(User.username, db.func.avg(Test.score).label('average_score')) \
        .join(Test, User.id == Test.user_id) \
        .filter(Test.course_id == course_id) \
        .group_by(User.username) \
        .order_by(db.desc('average_score')) \
        .all()

    user_average_scores = [{'username': username, 'average_score': average_score} for username, average_score in result]

    return jsonify({'average_scores': user_average_scores})

if __name__ == '__main__':
    # db.init_app(app)
    app.run(debug=True)
