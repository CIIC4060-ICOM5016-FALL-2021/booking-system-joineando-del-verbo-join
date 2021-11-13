from flask import jsonify
from model.users import UsersDAO
from datetime import datetime

class BaseUsers:

    def build_map_dict(self, row):
        result = {}
        result['userid'] = row[0]
        result['firstname'] = row[1]
        result['lastname'] = row[2]
        result['email'] = row[3]
        result['password'] = row[4]
        result['roleid'] = row[5]
        return result

    def build_map_dict_unaivalaible(self, row):
        result = {}
        result['startdatetime'] = row[0]
        result['enddatetime'] = row[1]
        return result

    def getAllUsers(self):
        dao = UsersDAO()
        users_tuple = dao.getAllUsers()
        result_list = []
        if not users_tuple:
            return jsonify("Not Found"), 404
        else:
            for user in users_tuple:
                result = self.build_map_dict(user)
                result_list.append(result)
            return jsonify(result), 200

    def addNewUser(self, json):
        firstname = json["firstname"]
        lastname = json["lastname"]
        email = json["email"]
        password = json["password"]
        roleid = json["roleid"]

        dao = UsersDAO()

        userid = dao.insertUser(firstname, lastname, email, password, roleid)
        tuple = (userid, firstname, lastname, email, password, roleid)
        result = self.build_map_dict(tuple)

        return jsonify(result), 200

    def updateUser(self, json, userid):
        firstname = json["firstname"]
        lastname = json["lastname"]
        email = json["email"]
        password = json["password"]
        roleid = json["roleid"]

        dao = UsersDAO()

        updated = dao.updateUser( firstname, lastname, email, password, roleid, userid,)
        result = self.build_map_dict((userid, firstname, lastname, email, password, roleid))
        if updated:
            return jsonify(result), 200
        else:
            return jsonify("NOT UPDATED"), 400

    def getUserByID(self, userid):
        dao = UsersDAO()
        user = dao.getUserByID(userid)
        result = self.build_map_dict(user)
        if user:
            return jsonify(result), 200
        else:
            return jsonify("Not Found"), 404


    def deleteUser(self, userid):
        dao = UsersDAO()
        result = dao.deleteUser(userid)
        if result:
            return jsonify("DELETED"), 200
        else:
            return jsonify("NOT FOUND"), 404

    def markTimeUnavailable(self, userid, json):
        startdatetime = json['startdatetime']
        enddatetime = json['enddatetime']
        startdatetime = datetime.strptime(startdatetime, "%Y-%m-%d %H:%M:%S.%f")
        enddatetime = datetime.strptime(enddatetime, "%Y-%m-%d %H:%M:%S.%f")
        dao = UsersDAO()
        time_busy = dao.markTimeUnavailable(userid,startdatetime,enddatetime)
        result = self.build_map_dict_unaivalaible(time_busy)
        return jsonify(result), 200

    def markTimeAvailable(self, userid, json):
        userunavailabilityid = json['userunavailabilityid']
        dao = UsersDAO()
        time_available = dao.markTimeAvailable(userid, userunavailabilityid)
        result = self.build_map_dict_unaivalaible(time_available)
        return jsonify(result), 200


