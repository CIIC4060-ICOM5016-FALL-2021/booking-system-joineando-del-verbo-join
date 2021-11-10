from flask import jsonify
from datetime import datetime
from model.users import UsersDAO
from model.reservation import ReservationDAO
from model.invitation import InvitationDAO

class BaseInvitation:

    def build_map_dict(self, row):
        result = {}
        result['inviteeid'] = row[0]
        result['reservationid'] = row[1]


    def createInvitation(self, json):
        inviteeid = json['inviteeid']
        reservationid = json['reservationid']

        dao = InvitationDAO()

        invited = dao.createInvitation(inviteeid, reservationid)

        if invited:
            result = self.build_map_dict((inviteeid, reservationid))
            return jsonify(result), 200
        else:
            return jsonify("Invitation not sent"), 400


