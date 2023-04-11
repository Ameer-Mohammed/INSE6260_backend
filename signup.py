from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:asdfgh@localhost/userdb'  # replace with your phpMyAdmin database URI
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))

    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.route('/signup', methods=['POST'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def signup():
    username = request.json['username']
    password = request.json['password']
    user = User(username, password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'})

@app.route('/users', methods=['GET'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def list_users():
    users = User.query.all()
    result = []
    for user in users:
        user_data = {}
        user_data['username'] = user.username
        user_data['password'] = user.password
        result.append(user_data)
    return jsonify(result)

@app.route('/user/login', methods=['POST'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def list_users2():
    username = request.json['username']
    password = request.json['password']
    users = User.query.all()
    
    for user in users:
        if user.username == username and user.password == password:
    # block of code if condition is True
            return jsonify({'authenticated': 'true'})
      
    return jsonify({'authenticated': 'false'})
   

if __name__ == '__main__':
    app.run(host="localhost", port=5001,debug=True)
