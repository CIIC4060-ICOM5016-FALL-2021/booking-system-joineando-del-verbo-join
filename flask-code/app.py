from flask import Flask, request, jsonify
from controller.users import BaseUsers
from controller.userrole import BaseUserRole
#from controller.room import BaseRoom
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/users', methods=['GET', 'POST'])
def handle_users():
    if request.method == 'GET':
         return BaseUsers().getAllUsers()
    elif request.method == 'POST':
         return BaseUsers().addNewUser(request.json)
    else:
        return jsonify("Method Not Allowed."), 405

@app.route('/userrole', methods=['POST'])
def handle_userrole():
    if request.method == 'POST':
        return BaseUserRole().addNewUserRole(request.json)
    else:
        return jsonify("Method Not Allowed."), 405


@app.route('/users/<int:userid>', methods=['PUT', 'GET', 'DELETE'])
def handle_usersid(userid):
    if request.method == 'PUT':
        return BaseUsers().updateUser(request.json, userid)
    elif request.method == 'GET':
        return BaseUsers().getUserByID(userid)
    elif request.method == 'DELETE':
        return BaseUsers().deleteUser(userid)

    else:
        return jsonify("Method Not Allowed."), 405

# @app.route('/room', methods=['POST', 'GET'])
# def handle_room():
#     if request.method == 'POST':
#         return BaseRoom().addNewRoom(request.json)
#     if request.method = 'GET':
#         return BaseRoom().getAllRooms()


#@app.route('/room/<int: ')


if __name__ == '__main__':
    app.run(debug=True)