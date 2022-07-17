from flask import Flask, make_response
from flask_restful import Api
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from db import *

app = Flask(__name__)
api = Api(app)
jwt = JWTManager(app)

app.config['SECRET_KEY'] = "root"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:root@localhost/postgres"

@app.route('/signup', methods=["POST"])
def signup():
 return(dbInsertUser())

@app.route('/login', methods=["POST"])
def login():
    data = request.get_json()
    user_name = data['username']
    user_password = data['password']
 
    user, user_pass= dbGetUserByName(user_name)

    if not user:
        return make_response("User doesn't exist")

    if bcrypt.check_password_hash(user_pass, user_password):
        token = create_access_token(identity=user_name)
        return jsonify({ "token": token })
    return make_response("incorrect password")

@app.route('/orders', methods=['POST'])
def place_order():
    data = request.get_json()
    return place_orders(data)

@app.route('/inventory', methods=['PUT'])
@jwt_required()
def inventory():
    return(items())

@app.route('/retrieve_orders', methods=['GET'])
@jwt_required()
def retrieve_order():
    return(check_orders())

if __name__ =="__main__":
    app.run(debug=True)
