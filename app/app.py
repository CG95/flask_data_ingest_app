from flask import Flask, jsonify, request
from . import create_app
from .models import User

app = create_app()


@app.route('/')
def index():
    users = User.query.all()
    return ','.join([user.name for user in users]) or "No users found"


@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or 'name' not in data or 'email' not in data or 'password' not in data:
        return jsonify({"error": "Invalid input"}), 400
    try:
        user = User.create(
            name=data['name'],
            email=data['email'],
            password=data['password'])
        return jsonify(user.to_dict()), 201
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
