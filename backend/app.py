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

@app.route('/joineando-del-verbo-join/users/login', methods=['POST'])
def handle_login():
    if request.method == 'POST':
        return BaseUsers().loginUser(request.json)
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

@app.route('/joineando-del-verbo-join/users/schedule/<int:userid>', methods=['GET'])
def handle_userschedule(userid):
    if request.method == 'GET':
        return BaseUsers().allDaySchedule(userid, request.json)
    else:
        return jsonify("METHOD NOT ALLOWED"), 405

@app.route('/joineando-del-verbo-join/users/marktimeunavailable/<int:userid>', methods=['POST', 'DELETE'])
def handle_timeunavailable(userid):
    if request.method == 'POST':
        return BaseUsers().markTimeUnavailable(userid, request.json)
    elif request.method == 'DELETE':
        return BaseUsers().markTimeAvailable(userid, request.json)
    else:
        return jsonify("METHOD NOT ALLOWED"), 405

@app.route('/joineando-del-verbo-join/usersunavailability', methods=['POST'])
def handle_usernavailability():
    if request.method == 'POST':
        return BaseUsers().checkUnavailableOnTimeFrame(request.json)
    else:
        return jsonify("METHOD NOT ALLOWED"), 405

#####################################################################
#                           USER ROLES                              #
#####################################################################
@app.route('/joineando-del-verbo-join/userroles', methods=['GET'])
def handle_userroles():
    if request.method == 'GET':
        return BaseUserRole().getAllUserRoles()
    else:
        return jsonify("METHOD NOT ALLOWED"), 405

@app.route('/joineando-del-verbo-join/userroles/<int:userroleid>', methods=['GET'])
def handle_userrole(userroleid):
    if request.method == 'GET':
        return BaseUserRole().getUserRolesByID(userroleid)
    else:
        return jsonify("METHOD NOT ALLOWED"), 405
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


@app.route('/joineando-del-verbo-join/room/availableroom', methods=['POST'])
def handle_availableroom():
    if request.method == 'POST':
        return BaseRoom().availableRoomAtTimeFrame(request.json)
    else:
        return jsonify("METHOD NOT ALLOWED"), 405

@app.route('/joineando-del-verbo-join/room/whoappointed/<int:roomid>', methods=['GET'])
def handle_whoappointed(roomid):
    if request.method == 'GET':
        return BaseRoom().whoAppointedRoom(roomid, request.json)
    else:
        return jsonify("METHOD NOT ALLOWED"), 405
#new route yet to verify ----------------------------------------------------------------------------------
@app.route('/joineando-del-verbo-join/room/makeroomunavailable/<int:roomid>', methods = ['POST'])
def handle_roomavailable(roomid):
    if request.method == 'POST':
        return BaseRoom().makeRoomUnavailable(roomid, request.json)
    else:
        return jsonify("METHOD NOT ALLOWED"), 405

#new route yet to verify -----------------------------------------------------------------------------------
@app.route('/joineando-del-verbo-join/room/makeroomavailable/', methods = ['DELETE'])
def handle_roomunavailable():
    if request.method == 'DELETE':
        return BaseRoom().makeRoomAvailable(request.json)
    else:
        return jsonify("METHOD NOT ALLOWED"), 405


@app.route('/joineando-del-verbo-join/room/schedule/<int:roomid>', methods=['GET'])
def handle_roomschedule(roomid):
    if request.method == 'GET':
        return BaseRoom().allDayScheduleRoom(roomid, request.json)
    else:
        return jsonify("METHOD NOT ALLOWED"), 405

@app.route('/joineando-del-verbo-join/getroomappointments/<int:roomid>', methods=['GET'])
def handle_room_appointments(roomid):
    if request.method == 'GET':
        return BaseReservation().getRoomAppointments(roomid, request.json)
    else:
        return jsonify('METHOD NOT ALLOWED', 405)

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

#####################################################################
#                          INVITATION                               #
#####################################################################

@app.route('/joineando-del-verbo-join/invitation', methods=['POST'])
def handle_invitation():
    if request.method == 'POST':
        return BaseInvitation().createInvitation(request.json)
    else:
        return jsonify("METHOD NOT ALLOWED"), 405

@app.route('/joineando-del-verbo-join/invitation/<int:inviteeid>/<int:reservationid>', methods=['GET','DELETE'])
def handle_invitations(reservationid, inviteeid):
    if request.method == 'GET':
        return BaseInvitation().getInvitationByID(inviteeid, reservationid)
    elif request.method == 'DELETE':
        return BaseInvitation().deleteInvitation(inviteeid, reservationid)
    else:
        return jsonify("METHOD NOT ALLOWED"), 405


#####################################################################
#                         STATISTICS                                #
#####################################################################
@app.route('/joineando-del-verbo-join/users/stats/mostusedroom/<int:userid>', methods = ['GET'])
def handle_mostusedroom(userid):
    if request.method == 'GET':
        return BaseUsers().userMostUsedRoom(userid)
    else:
        return jsonify('METHOD NOT ALLOWED'), 405


@app.route('/joineando-del-verbo-join/users/stats/mostreservations/<int:userid>', methods = ['GET'])
def handle_usermostreservations(userid):
    if request.method == 'GET':
        return BaseUsers().userWithMostReservation(userid)
    else:
        return jsonify('METHOD NOT ALLOWED'), 405


@app.route('/joineando-del-verbo-join/users/stats/topten', methods = ['GET'])
def handle_userstopten():
    if request.method == 'GET':
        return BaseUsers().usersTopTen()
    else:
        return jsonify('METHOD NOT ALLOWED'), 405

@app.route('/joineando-del-verbo-join/room/stats/topten', methods = ['GET'])
def handle_roomtopten():
    if request.method == 'GET':
        return BaseRoom().roomTopTen()
    else:
        return jsonify('METHOD NOT ALLOWED'), 405


@app.route('/joineando-del-verbo-join/reservation/stats/busiesthours', methods = ['GET'])
def handle_busiesthours():
    if request.method == 'GET':
        return BaseReservation().busiestHours()
    else:
        return jsonify('METHOD NOT ALLOWED'), 405


if __name__ == '__main__':
    app.run(debug=True)

