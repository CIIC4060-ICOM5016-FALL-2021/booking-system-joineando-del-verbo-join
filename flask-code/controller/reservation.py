from flask import jsonify
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

        dao = ReservationDAO()

        reservationid = dao.createReservation(hostid, roomid, reservationname, startdatetime, enddatetime)
        result = self.build_map_dict((reservationid, hostid, roomid, reservationname, startdatetime, enddatetime))
        return jsonify(result), 200

    def updateReservation(self, json, reservationid):
        hostid = json["hostid"]
        roomid = json["roomid"]
        reservationname = json["reservationname"]
        startdatetime = json["startdatetime"]
        enddatetime = json["enddatetime"]

        dao = ReservationDAO()

        updated = dao.updateReservation(reservationid, hostid, roomid, reservationname, startdatetime, enddatetime)
        result = self.build_map_dict((reservationid, hostid, roomid, reservationname, startdatetime, enddatetime))
        if updated:
            return jsonify(result), 200
        else:
            return jsonify("NOT UPDATED"), 400
