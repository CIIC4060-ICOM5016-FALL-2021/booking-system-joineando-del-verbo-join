from flask import jsonify
from model.users import UsersDAO
from datetime import datetime, date, time, timedelta

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

    def build_map_dict_checkunaivalaible(self, row):
        result = {}
        result['userid'] = row[0]
        result['startdatetime'] = row[1]
        result['enddatetime'] = row[2]
        return result


    def build_map_dict_mostreservations(self, row):
        result = {}
        result['userid'] = row[0]
        result['firstname'] = row[1]
        result['lastname'] = row[2]
        result['email'] = row[3]
        result['meetings'] = row[4]
        return result

    def build_map_dict_mostusedroom(self, row):
        result = {}
        result['roomid'] = row[0]
        result['buildingname'] = row[1]
        result['roomnumber'] = row[2]
        return result



    # verified

    def getAllUsers(self):
        dao = UsersDAO()
        users_tuple = dao.getAllUsers()
        result_list = []
        if not users_tuple:
            dao.conn.close()
            return jsonify("NOT FOUND"), 404
        else:
            for user in users_tuple:
                result = self.build_map_dict(user)
                result_list.append(result)
            dao.conn.close()
            return jsonify(result_list), 200

    # verified
    def addNewUser(self, json):
        firstname = json["firstname"]
        lastname = json["lastname"]
        email = json["email"]
        password = json["password"]
        roleid = json["roleid"]

        dao = UsersDAO()

        userid = dao.insertUser(firstname, lastname, email, password, roleid)
        if userid:
            user_tuple = (userid, firstname, lastname, email, password, roleid)
            result = self.build_map_dict(user_tuple)
            dao.conn.close()
            return jsonify(result), 200
        else:
            dao.conn.close()
            return jsonify("USER NOT CREATED"), 500

    # verified
    def updateUser(self, json, userid):
        firstname = json["firstname"]
        lastname = json["lastname"]
        email = json["email"]
        password = json["password"]
        roleid = json["roleid"]

        dao = UsersDAO()

        updated = dao.updateUser( firstname, lastname, email, password, roleid, userid,)
        if updated:
            result = self.build_map_dict((userid, firstname, lastname, email, password, roleid))
            dao.conn.close()
            return jsonify(result), 200
        else:
            dao.conn.close()
            return jsonify("USER NOT FOUND"), 404

    # verified
    def getUserByID(self, userid):
        dao = UsersDAO()
        user = dao.getUserByID(userid)
        if user:
            result = self.build_map_dict(user)

            return jsonify(result), 200
        else:

            return jsonify("USER NOT FOUND"), 404


    def deleteUser(self, userid):
        dao = UsersDAO()
        result = dao.deleteUser(userid)
        if result:
            dao.conn.close()
            return jsonify("DELETED USER"), 200
        else:
            dao.conn.close()
            return jsonify("USER NOT FOUND"), 404

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


    def allDaySchedule(self, userid, json):
        daystart = json['daystart']
        daystart = datetime.strptime(daystart, "%Y-%m-%d %H:%M:%S.%f")
        dayend = daystart + timedelta(days=1)
        dao = UsersDAO()
        schedule_tuple = dao.allDaySchedule(userid, daystart, dayend)
        result_list = []
        if not schedule_tuple:
            return jsonify("NO SCHEDULE"), 404
        else:
            for time in schedule_tuple:
                result = self.build_map_dict_unaivalaible(time)
                result_list.append(result)
            return jsonify(result_list), 200


    #statistics

    def userWithMostReservation(self):
        dao = UsersDAO()
        tuple = dao.userWithMostReservation()
        result = self.build_map_dict_mostreservations(tuple)
        return jsonify(result), 200

    def usersTopTen(self):
        dao = UsersDAO()
        tuples = dao.userTopTen()
        result = []
        if not tuples:
            return jsonify("Not Found"), 404
        else:
            for row in tuples:
                result.append(self.build_map_dict_mostreservations(row))
            return jsonify(result), 200

    def userMostUsedRoom(self, userid):
        dao = UsersDAO()
        tuple = dao.userMostUsedRoom(userid)
        if not tuple:
            return jsonify("No Result Found."), 404
        else:
            result = self.build_map_dict_mostusedroom(tuple)
            return jsonify(result), 200

    def checkUnavailableOnTimeFrame(self, json):
        dao = UsersDAO()
        users = json['usersIDs']
        startdatetime = json['startdatetime']
        enddatetime = json['enddatetime']
        times = []
        for userid in users:
            temp = dao.checkUnavailableOnTimeFrame(userid, startdatetime, enddatetime)
            if temp:
                times += temp

        result = []
        for item in times:
            result.append(self.build_map_dict_checkunaivalaible(item))

        return jsonify(result), 200



