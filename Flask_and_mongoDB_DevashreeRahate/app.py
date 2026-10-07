from flask import Flask, request, render_template, jsonify
from datetime import datetime
from pymongo import MongoClient
import json

app = Flask(__name__)

# MongoDB Atlas Connection


MONGO_URI = "mongodb+srv://FLASK:DEVASHREE@cluster0.xaoxhff.mongodb.net/"
client = MongoClient(MONGO_URI)

db = client["signup_database"]
users_collection = db["users"]
todo_collection = db["todoitems"]


# Home Page

@app.route('/')
def home():
    day_of_week = datetime.now().strftime("%A")
    current_time = datetime.now().strftime("%H:%M:%S")

    return render_template(
        'index.html',
        day_of_week=day_of_week,
        current_time=current_time
    )

# Task 1: JSON API Route

@app.route('/api')
def api():

    try:
        # Open the backend JSON file
        with open('data.json', 'r') as file:

            # Read the JSON data
            data = json.load(file)

        # Send data as JSON response
        return jsonify(data)

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

# Task 2: Form Submission

@app.route('/submit', methods=['POST'])
def submit():

    try:
        # Get data from the form
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Check if all fields are filled
        if not name or not email or not password or not confirm_password:
            return render_template(
                'index.html',
                error="All fields are required.",
                day_of_week=datetime.now().strftime("%A"),
                current_time=datetime.now().strftime("%H:%M:%S")
            )

        # Check whether passwords match
        if password != confirm_password:
            return render_template(
                'index.html',
                error="Passwords do not match.",
                day_of_week=datetime.now().strftime("%A"),
                current_time=datetime.now().strftime("%H:%M:%S")
            )

        # Data to be inserted into MongoDB
        user_data = {
            "name": name,
            "email": email,
            "password": password
        }

        # Insert data into MongoDB Atlas
        users_collection.insert_one(user_data)

        # If insertion is successful
        return render_template('success.html')

    except Exception as e:

        # If an error occurs, stay on the same page
        return render_template(
            'index.html',
            error="Error: " + str(e),
            day_of_week=datetime.now().strftime("%A"),
            current_time=datetime.now().strftime("%H:%M:%S")
        )

@app.route('/submittodoitem', methods=['POST'])
def submit_todo_item():
    data = request.get_json()

    item_name = data.get('itemName')
    item_description = data.get('itemDescription')

    todo_collection.insert_one({
        "itemName": item_name,
        "itemDescription": item_description
    })

    return jsonify({
        "message": "To-Do item submitted successfully"
    }), 201
    
# todo 
@app.route('/todo')
def todo():
    return render_template('todo.html')

# Run Flask Application

if __name__ == '__main__':
    app.run(debug=True)