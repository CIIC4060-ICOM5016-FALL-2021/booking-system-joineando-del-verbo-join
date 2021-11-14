from flask import Flask, request, jsonify
from controller.users import BaseUsers
from controller.userrole import BaseUserRole
from controller.reservation import BaseReservation
from controller.room import BaseRoom
from flask_cors import CORS
from controller.invitation import BaseInvitation

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():  # put application's code here
    return 'Booking-App by Joineando del Verbo Join '

#####################################################################
#                               USERS                               #
#####################################################################
# verified
@app.route('/joineando-del-verbo-join/users', methods=['GET', 'POST'])
def handle_users():
    if request.method == 'GET':
        return BaseUsers().getAllUsers()
    elif request.method == 'POST':
        return BaseUsers().addNewUser(request.json)
    else:
        return jsonify("METHOD NOT ALLOWED"), 405

# verified
@app.route('/joineando-del-verbo-join/users/<int:userid>', methods=['PUT', 'GET', 'DELETE'])
def handle_usersid(userid):
    if request.method == 'PUT':
        return BaseUsers().updateUser(request.json, userid)
    elif request.method == 'GET':
        return BaseUsers().getUserByID(userid)
    elif request.method == 'DELETE':
        return BaseUsers().deleteUser(userid)
    else:
        return jsonify("METHOD NOT ALLOWED"), 405

@app.route('/users/marktimeunavailable/<int:userid>', methods=['PUT', 'DELETE'])
def handle_timeunavailable(userid):
    if request.method == 'PUT':
        return BaseUsers().markTimeUnavailable(userid, request.json)
    elif request.method == 'DELETE':
        return BaseUsers().markTimeAvailable(userid, request.json)
    else:
        return jsonify("Method Not Allowed."), 405

#####################################################################
#                              ROOM                                 #
#####################################################################
# verified
@app.route('/joineando-del-verbo-join/room', methods=['POST', 'GET'])
def handle_room():
    if request.method == 'POST':
        return BaseRoom().addNewRoom(request.json)
    if request.method == 'GET':
        return BaseRoom().getAllRooms()
    else:
        return jsonify("METHOD NOT ALLOWED"), 405
# verified
@app.route('/joineando-del-verbo-join/room/<int:roomid>', methods=['PUT', 'GET', 'DELETE'])
def handle_roomid(roomid):
    if request.method == 'PUT':
        return BaseRoom().updateRoom(request.json, roomid)
    elif request.method == 'GET':
        return BaseRoom().getRoomByID(roomid)
    elif request.method == 'DELETE':
        return BaseRoom().deleteRoom(roomid)
    else:
        return jsonify("METHOD NOT ALLOWED"), 405


#####################################################################
#                          RESERVATION                              #
#####################################################################
@app.route('/joineando-del-verbo-join/reservation', methods=['POST'])
def handle_reservation():
    if request.method == 'POST':
        return BaseReservation().addNewReservation(request.json)
    else:
        return jsonify("METHOD NOT ALLOWED"), 405


@app.route('/joineando-del-verbo-join/reservation/<int:reservationid>', methods=['PUT', 'DELETE', 'GET'])
def handle_reservationid(reservationid):
    if request.method == 'PUT':
        return BaseReservation().updateReservation(request.json, reservationid)
    elif request.method == 'DELETE':
        return BaseReservation().deleteReservation(reservationid)
    elif request.method == 'GET':
        return BaseReservation().getReservationByID(reservationid)
    else:
        return jsonify("METHOD NOT ALLOWED"), 405

@app.route('/room/schedule/<int:roomid>', methods=['GET'])
def handle_roomschedule(roomid):
    if request.method == 'GET':
        return BaseRoom().allDayScheduleRoom(roomid)
    else:
        return jsonify("METHOD NOT ALLOWED"), 405





@app.route('/room/whoappointed/<int:roomid>', methods=['GET'])
def handle_whoappointed(roomid):
    if request.method == 'GET':
        return BaseRoom().whoAppointedRoom(roomid, request.json)
    else:
        return jsonify("METHOD NOT ALLOWED"), 405

@app.route('/room/availableroom', methods=['GET'])
def handle_availableroom():
    if request.method == 'GET':
        return BaseRoom().availableRoomAtTimeFrame(request.json)
    else:
        return jsonify("Method Not Allowed."), 405

@app.route('/invitation', methods=['POST'])
def handle_invitation():
    if request.method == 'POST':
        return BaseInvitation().createInvitation(request.json)
    else:
        return jsonify("Method Not Allowed."), 405

@app.route('/invitation/<int:reservationid>', methods=['GET','PUT'])
def handle_invitations(reservationid):
    if request.method == 'GET':
        return BaseInvitation().allInviteesForReservation(reservationid)
    elif request.method == 'PUT':
        return BaseInvitation().updateInvitation(reservationid, request.json)
    else:
        return jsonify('Method Not Allowed.'), 405


@app.route('/users/stats/mostreservations', methods = ['GET'])
def handle_usermostreservations():
    if request.method == 'GET':
        return BaseUsers().userWithMostReservation()
    else:
        return jsonify('Method Not Allowed.', 405)

@app.route('/users/stats/topten', methods = ['GET'])
def handle_userstopten():
    if request.method == 'GET':
        return BaseUsers().usersTopTen()
    else:
        return jsonify('Method Not Allowed.', 405)

@app.route('/room/stats/topten', methods = ['GET'])
def handle_roomtopten():
    if request.method == 'GET':
        return BaseRoom().roomTopTen()
    else:
        return jsonify('Method Not Allowed.', 405)

@app.route('/users/stats/mostusedroom/<int:userid>', methods = ['GET'])
def handle_mostusedroom(userid):
    if request.method == 'GET':
        return BaseUsers().userMostUsedRoom(userid)
    else:
        return jsonify('Method Not Allowed.', 405)

@app.route('/reservation/stats/busiesthours', methods = ['GET'])
def handle_busiesthours():
    if request.method == 'GET':
        return BaseReservation().busiestHours()
    else:
        return jsonify('Method Not Allowed.', 405)


@app.route('/invitation/<int:reservationid>/<int:inviteeid>', methods=['DELETE'])
def handle_invitations_delete(reservationid,inviteeid):
    if request.method == 'DELETE':
        return BaseInvitation().deleteInvitation(inviteeid,reservationid)
    else:
        return jsonify("Method Not Allowed."), 405


if __name__ == '__main__':
    app.run(debug=True)

