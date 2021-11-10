from flask import jsonify
from datetime import datetime
from model.users import UsersDAO
from model.reservation import ReservationDAO


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


    def addNewReservation(self, json):
        hostid = json["hostid"]
        roomid = json["roomid"]
        reservationname = json["reservationname"]
        startdatetime = json["startdatetime"]
        enddatetime = json["enddatetime"]



        start = datetime.strptime(startdatetime, "%Y-%m-%d %H:%M:%S.%f")
        end = datetime.strptime(enddatetime, "%Y-%m-%d %H:%M:%S.%f")
        if start > end:
            return jsonify("END TIME SHOULD BE AFTER START TIME"), 400

        userDAO = UsersDAO()
        hostAvailable = userDAO.checkUserAvailability(hostid, startdatetime, enddatetime)
        if not hostAvailable:
            return jsonify("TIMESLOT NOT AVAILABLE"), 400

        dao = ReservationDAO()

        reservationid = dao.createReservation(hostid, roomid, reservationname, startdatetime, enddatetime)

        if reservationid:
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

        dao = ReservationDAO()

        updated = dao.updateReservation(reservationid, hostid, roomid, reservationname, startdatetime, enddatetime)
        if updated:
            result = self.build_map_dict((reservationid, hostid, roomid, reservationname, startdatetime, enddatetime))
            return jsonify(result), 200
        else:
            return jsonify("NOT UPDATED"), 400


    def deleteReservation(self, reservatioid):
        dao = ReservationDAO()
        result = dao.deleteReservation(reservatioid)
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
            return jsonify("Not Found"), 404


