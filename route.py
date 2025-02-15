from flask import render_template, request, redirect, url_for, flash # Import render_template, request, redirect, url_for, and flash
from . import app, db  # Import app and db from the skillshare package
from skillshare import app, db  # Import app and db from the skillshare package
from .models import User, Skill, Message # Import the User, Skill, and Message models
from werkzeug.security import generate_password_hash, check_password_hash # For password hashing
from flask_login import login_user, LoginManager, login_required, logout_user, current_user # For Login Management


# Initialize Flask-Login
login_manager = LoginManager() # Create a Login Manager instance
login_manager.init_app(app) # Initialize the Login Manager with the Flask app
login_manager.login_view = 'login' # Where to redirect if not logged in

@login_manager.user_loader # How to load a user
def load_user(user_id): # Define the load_user function
    return User.query.get(int(user_id)) # How to load a user object

@app.route('/') # Route for the main page (/)
def index(): # Define the index function
    return render_template('index.html') # Render the index.html template

@app.route('/register', methods=['GET', 'POST']) # Route for the registration page
def register(): # Define the register function
    if request.method == 'POST': # If the form is submitted
        username = request.form['username'] # Get the username from the form
        password = request.form['password'] # Get the password from the form
        school = request.form['school'] # Get the school from the form
        year = request.form['year'] # Get the year from the form
        bio = request.form['bio'] # Get the bio from the form

        # Check if user already exists
        if User.query.filter_by(username=username).first(): # Check if the username already exists
            flash('Username already exists. Please choose a different one.') # Flash a message
            return redirect(url_for('register')) # Redirect to the registration page

        # Hash the password before storing it
        hashed_password = generate_password_hash(password, method='sha256') # Hash the password

        new_user = User(username=username, password=hashed_password, school=school, year=year, bio=bio) # Create a new user object
        db.session.add(new_user) # Add the new user to the database
        db.session.commit() # Commit the changes
        return redirect(url_for('login'))  # Redirect to login after registration

    return render_template('registration.html') # Render the registration.html template

@app.route('/login', methods=['GET', 'POST']) # Route for the login page
def login(): # Define the login function
    if request.method == 'POST': # If the form is submitted
        username = request.form['username'] # Get the username from the form
        password = request.form['password'] # Get the password from the form
        user = User.query.filter_by(username=username).first() # Query the database for the user

        if user and check_password_hash(user.password, password): # Check hashed password
            login_user(user) # Log the user in
            return redirect(url_for('profile'))  # Redirect to the profile page
        else: # If the user doesn't exist or password is wrong
            flash('Invalid username or password') # Flash a message

    return render_template('login.html') # Render the login.html template

@app.route('/logout') # Route for the logout page
@login_required # Protect the logout route; user must be logged in
def logout(): # Define the logout function
    logout_user() # Log the user out using Flask-Login
    return redirect(url_for('index')) # Redirect to the index page after logout

@app.route('/profile')
@login_required  # Protect the profile route; user must be logged in
def profile(): # Define the profile function
    return render_template('profile.html') # Render the profile.html template

@app.route('/skills') # Route for the skills page
def skills(): # Define the skills function
    return "Skills Page" # Replace with your actual skills page content

if __name__ == '__main__': # If this file is run directly
    app.run(debug=True) # Start the Flask app in debug mode
    # app.run(debug=False) # Start the Flask app in production mode