from flask import jsonify
from datetime import datetime
from model.users import UsersDAO
from model.reservation import ReservationDAO
from model.invitation import InvitationDAO
from datetime import datetime

class BaseInvitation:

    def build_map_dict(self, row):
        result = {}
        result['reservationname'] = row[0]
        result['startdatetime'] = row[1]
        result['enddatetime'] = row[2]
        return result

    def build_map_dict_user(self, row):
        result = {}
        result['userid'] = row[0]
        result['firstname'] = row[1]
        result['lastname'] = row[2]
        return result

    def build_map_dict_update(self,row):
        result = {}
        result['reservationid'] = row[0]
        result['startdatetime'] = row[1]
        result['enddatetime'] = row[2]
        return result
    def build_map_dict_delete(self, row):
        result = {}
        result['userid'] = row[0]
        result['reservationid'] = row[1]
        return result

    def createInvitation(self, json):
        inviteeid = json['inviteeid']
        reservationid = json['reservationid']
        startdatetime = json['startdatetime']
        enddatetime = json['enddatetime']
        startdatetime = datetime.strptime(startdatetime, "%Y-%m-%d %H:%M:%S.%f")
        enddatetime = datetime.strptime(enddatetime, "%Y-%m-%d %H:%M:%S.%f")
        dao = InvitationDAO()
        invited = dao.createInvitation(inviteeid, reservationid, startdatetime, enddatetime)
        result = self.build_map_dict(invited)
        return jsonify(result), 200

    def allInviteesForReservation(self, reservationid):
        dao = InvitationDAO()
        invitation_list = dao.allInviteesForReservation(reservationid)
        result_list = []
        for row in invitation_list:
            obj = self.build_map_dict_user(row)
            result_list.append(obj)
        return jsonify(result_list), 200

    def updateInvitation(self, reservationid, json):
        startdatetime = json['startdatetime']
        enddatetime = json['enddatetime']
        startdatetime = datetime.strptime(startdatetime, "%Y-%m-%d %H:%M:%S.%f")
        enddatetime = datetime.strptime(enddatetime, "%Y-%m-%d %H:%M:%S.%f")
        dao = InvitationDAO()
        updated = dao.updateInvitation(reservationid, startdatetime, enddatetime)
        if updated:
            result = self.build_map_dict_update((reservationid, startdatetime,enddatetime))
            return jsonify(result), 200
        else:
            return jsonify("INVITATION NOT UPDATED"), 404

    def deleteInvitation(self, userid, reservationid):
        dao = InvitationDAO()
        deleted = dao.deleteInvitation(userid, reservationid)
        if deleted:
            result = self.build_map_dict_delete((userid, reservationid))
            return jsonify(result), 200
        else:
            return jsonify("COULD NOT DELELETE USER"), 404













