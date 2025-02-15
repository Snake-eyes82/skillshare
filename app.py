from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
# from skillshare import app

from models import User, Skill, Message  # Import models *AFTER* db is initialized

app = Flask(__name__)

secret_key = os.urandom(24)
app.config['SECRET_KEY'] = secret_key

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../instance/skillshare.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app) # Initialize SQLAlchemy *AFTER* app is created
# db.init_app(app)  # Initialize db with app

# from .models import User, Skill, Message  # Import models *AFTER* db is initialized
# from models import db # import db after init_app

def create_tables_if_not_exist():
    with app.app_context():
        inspector = db.inspect(db.engine)  # Get an Inspector object
        if not inspector.has_table('users'):  # Check if *any* table exists
            db.create_all()  # Create all table

@app.route('/')  # Route for the main page (/)
def index():
    create_tables_if_not_exist()
    return render_template('index.html')  # Render the index.html template

# @app.before_first_request
# def create_tables():
#     with app.app_context():
#         db.create_all()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        school = request.form.get('school')
        year = request.form.get('year')
        bio = request.form.get('bio')
        print(request.form)  # Add this line for debugging!!!

        # Validate data (now inside the POST block):
        if not username or username.strip() == "":  # Check for empty strings as well
            return jsonify({'error': 'Username is required'}), 400
        if not password or password.strip() == "":
            return jsonify({'error': 'Password is required'}), 400
        if not school or school.strip() == "":
            return jsonify({'error': 'School is required'}), 400
        if not year:  # No need to check for empty string for a number
            return jsonify({'error': 'Year is required'}), 400
        if not bio or bio.strip() == "":
            return jsonify({'error': 'Bio is required'}), 400

        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'Username already exists'}), 400

        password_hash = generate_password_hash(password)
        new_user = User(username=username, password_hash=password_hash, school=school, year=year, bio=bio)

        try:
            with app.app_context(): # Explcititly use app context
                db.session.add(new_user)
                db.session.commit()
            return jsonify({'message': 'User registered successfully'}), 201  # Return success message

        except Exception as e:
            db.session.rollback()
            print(f"Error during registration: {e}")  # Log the error for debugging
            return jsonify({'error': 'An error occurred during registration'}), 500  # Generic error message for the client
            #return jsonify({'error': str(e)}), 500

    return render_template('registration.html')  # For GET requests (no validation here)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            return jsonify({'message': 'Login successful'}), 200 # JSON success (even though redirect follows)
        else:
            return jsonify({'error': 'Invalid username or password'}), 401  # JSON error

    return render_template('login.html')  # This is OK for GET requests


@app.route('/profile')
def profile():
    user_id = session.get('user_id')  # Get user ID from the session
    if user_id:
        user = User.query.get(user_id)  # Retrieve user from the database
        return render_template('profile.html', user=user)  # Pass user to the template
    else:
        return "You are not logged in."  # Or redirect to the login page  # User not logged in


# ... (Other routes for login, skill management, messaging, etc.)

if __name__ == '__main__':
    create_tables_if_not_exist() # Call it here too, just in case the / route is never hit.
    app.run(debug=True)  # debug=True for development