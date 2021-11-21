from flask import jsonify
from datetime import datetime
from model.users import UsersDAO
from model.reservation import ReservationDAO
from model.room import RoomDAO
from model.invitation import InvitationDAO


class BaseReservation:

    def build_map_dict(self, row):
        result = {}
        result['reservationid'] = row[0]
        result['hostid'] = row[1]
        result['roomid'] = row[2]
        result['reservationname'] = row[3]
        result['startdatetime'] = row[4]
        result['enddatetime'] = row[5]
        return result


    def reservationPreCheck(self, hostid, roomid, startdatetime, enddatetime, inviteesIds):
        start = datetime.strptime(startdatetime, "%Y-%m-%d %H:%M:%S.%f")
        end = datetime.strptime(enddatetime, "%Y-%m-%d %H:%M:%S.%f")
        if start > end:
            return jsonify("END TIME SHOULD BE AFTER START TIME"), 400

        userDAO = UsersDAO()
        hostAvailable = userDAO.checkUserAvailability(hostid, startdatetime, enddatetime)
        if not hostAvailable:
            return jsonify("TIMESLOT NOT AVAILABLE FOR HOST"), 400

        for invitee in inviteesIds:
            if not userDAO.checkUserAvailability(invitee, startdatetime, enddatetime):
                return jsonify("TIMESLOT NOT AVAILABLE FOR A INVITEE: ", invitee), 400       # change for privacy later


        roomDAO = RoomDAO()
        roomAvailable = roomDAO.checkRoomAvailability(roomid, startdatetime, enddatetime)
        if not roomAvailable:
            return jsonify("TIMESLOT NOT AVAILABLE IN ROOM"), 400

        return "OK"


    def addNewReservation(self, json):
        hostid = json["hostid"]
        roomid = json["roomid"]
        reservationname = json["reservationname"]
        startdatetime = json["startdatetime"]
        enddatetime = json["enddatetime"]
        inviteesIds = json["inviteesIds"]

        precheck = self.reservationPreCheck(hostid, roomid, startdatetime, enddatetime, inviteesIds)

        if precheck != "OK":
            return precheck

        dao = ReservationDAO()
        reservationid = dao.createReservation(hostid, roomid, reservationname, startdatetime, enddatetime)

        if reservationid:
            invitationDao = InvitationDAO()
            for invitee in inviteesIds:
                if invitee != hostid:
                    invitationDao.createInvitation(invitee, reservationid)

            result = self.build_map_dict((reservationid, hostid, roomid, reservationname, startdatetime, enddatetime))
            return jsonify(result), 200
        else:
            return jsonify("NOT CREATED"), 400


    def updateReservation(self, json, reservationid):
        hostid = json["hostid"]
        roomid = json["roomid"]
        reservationname = json["reservationname"]
        startdatetime = json["startdatetime"]
        enddatetime = json["enddatetime"]

        invDAO = InvitationDAO()
        result = invDAO.allInviteesForReservation(reservationid)

        invitees = []
        for row in result:
            invitees.append(row[0])

        dao = ReservationDAO()
        if dao.didChangeTime(reservationid, startdatetime, enddatetime):
            precheck = self.reservationPreCheck(hostid, roomid, startdatetime, enddatetime, invitees)

            if precheck != "OK":
                return precheck

        updated = dao.updateReservation(reservationid, hostid, roomid, reservationname, startdatetime, enddatetime)
        if updated:
            result = self.build_map_dict((reservationid, hostid, roomid, reservationname, startdatetime, enddatetime))
            return jsonify(result), 200
        else:
            return jsonify("NOT UPDATED"), 400


    def deleteReservation(self, reservationid):
        dao = ReservationDAO()
        invitationDAO = InvitationDAO()

        inviteedIds = invitationDAO.allInviteesForReservation(reservationid)
        for user in inviteedIds:
            invitationDAO.deleteInvitation(user[0], reservationid)

        result = dao.deleteReservation(reservationid)
        if result:
            return jsonify("DELETED"), 200
        else:
            return jsonify("NOT FOUND"), 404


    def getReservationByID(self, reservationid):
        dao = ReservationDAO()
        reservation = dao.getReservationByID(reservationid)
        if reservation:
            result = self.build_map_dict(reservation)
            return jsonify(result), 200
        else:
            return jsonify("NOT FOUND RESERVATION"), 404


    def busiestHours(self):
        dao = ReservationDAO()
        busiest_hours = dao.busiestHours()
        result = []
        for row in busiest_hours:
            result.append({"hour": row[0]})
        return jsonify(result), 200

    def getRoomAppointments(self, roomid, json):
        userID = json["userid"]
        userDao = UsersDAO()
        user = userDao.getUserByID(userID)

        if user[5] == 3:
            reservationDao = ReservationDAO()
            appointments = reservationDao.getRoomAppointments(roomid)
            if appointments:
                result = []
                for row in appointments:
                    result.append(self.build_map_dict(row))
                return jsonify(result), 200
            else:
                return jsonify("APPOINTMENTS NOT FOUND"), 404
        else:
            return jsonify("ACCESS DENIED"), 403


