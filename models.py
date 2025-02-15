from flask_sqlalchemy import SQLAlchemy # Import SQLAlchemy
from flask_login import UserMixin # Import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash # Import password hashing functions
# from skillshare import db # Import the db object from the __init__.py file

db = SQLAlchemy() # Initialize SQLAlchemy

class User(db.Model): # Added User model
    __tablename__ = 'users' # Define the table name
    id = db.Column(db.Integer, primary_key=True) # Added primary_key=True
    username = db.Column(db.String, unique=True, nullable=False) # Added unique=True
    password_hash = db.Column(db.String, nullable=False) # Changed from password to password_hash
    school = db.Column(db.String) # Added school
    year = db.Column(db.Integer) # Added year
    bio = db.Column(db.Text) # Added bio

    skills = db.relationship('Skill', backref='user', lazy=True) # Added skills relationship
    messages_sent = db.relationship('Message', backref='sender', lazy=True, foreign_keys='Message.sender_id') # Corrected
    messages_received = db.relationship('Message', backref='receiver', lazy=True, foreign_keys='Message.receiver_id')  # Corrected

    def __repr__(self): # Added __repr__ method
        # return f'<User {self.username}>'
        return '<User %r>' % self.username # Changed to use %r

class Skill(db.Model): # Added Skill model
    __tablename__ = 'skills' # Define the table name
    id = db.Column(db.Integer, primary_key=True) # Added primary_key=True
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) # Added user_id
    skill_name = db.Column(db.String, nullable=False) # Added skill_name
    description = db.Column(db.Text) # Added description
    rate = db.Column(db.Numeric) # Added rate
    availability = db.Column(db.Text) # Added availability

    def __repr__(self): # Added __repr__ method
        return f'<Skill {self.skill_name}>' # Return the skill name

class Message(db.Model): # Added Message model
    __tablename__ = 'messages' # Define the table name
    id = db.Column(db.Integer, primary_key=True) # Added primary_key=True
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) # Added sender_id
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) # Added receiver_id
    message_text = db.Column(db.Text) # Added message_text
    timestamp = db.Column(db.DateTime) # Added timestamp

    def __repr__(self): # Added __repr__ method
        return f'<Message from {self.sender_id} to {self.receiver_id}>' # Return the message details