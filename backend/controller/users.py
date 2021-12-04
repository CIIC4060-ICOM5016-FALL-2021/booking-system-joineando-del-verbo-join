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

    def build_map_login(self, row):
        result = {}
        result['userid'] = row[0]
        result['firstname'] = row[1]
        result['lastname'] = row[2]
        return result

    def build_map_dict_unavailable(self, row):
        result = {}
        result['startdatetime'] = row[0]
        result['enddatetime'] = row[1]
        result['userunavailabilityid'] = row[2]
        return result

    def build_map_dict_available(self, row):
        result = {}
        result['startdatetime'] = row[0]
        result['enddatetime'] = row[1]
        return result

    def build_map_dict_checkunavailable(self, row):
        result = {}
        result['userid'] = row[0]
        result['startdatetime'] = row[1]
        result['enddatetime'] = row[2]
        return result

    # changed
    def build_map_dict_mostreservations(self, row):
        result = {}
        result['userid'] = row[0]
        result['firstname'] = row[1]
        result['lastname'] = row[2]
        result['email'] = row[3]
        result['appointments'] = row[4]
        return result

    def build_map_dict_mostusedroom(self, row):
        result = {}
        result['roomid'] = row[0]
        result['buildingname'] = row[1]
        result['roomnumber'] = row[2]
        return result

    # added
    def build_map_dict_schedule(self, row):
        result = {}
        result["reservationid"] = row[0]
        result["reservationname"] = row[1]
        result["roomid"] = row[2]
        result["startdatetime"] = row[3]
        result["enddatetime"] = row[4]
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
        if userid == -200:
            dao.conn.close()
            return jsonify("EMAIL ALREADY IN USE"), 400
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
        if result == -200:
            dao.conn.close()
            return jsonify("USER HAS MEETINGS"), 400
        elif result:
            dao.conn.close()
            return jsonify("DELETED USER"), 200

        else:
            dao.conn.close()
            return jsonify("USER NOT FOUND"), 404

    def loginUser(self, json):
        email = json["email"]
        password = json["password"]
        dao = UsersDAO()
        result = dao.loginUser(email, password)
        if result:
            dao.conn.close()
            user = self.build_map_login(result)
            return jsonify(user), 200
        else:
            return jsonify("INVALID CREDENTIALS"), 500

    # changed
    def markTimeUnavailable(self, userid, json):#######################################################################
        #loggeduserid = json['loggeduserid']
        startdatetime = json['startdatetime']
        enddatetime = json['enddatetime']
        startdatetime = datetime.strptime(startdatetime, "%Y-%m-%d %H:%M:%S.%f")
        enddatetime = datetime.strptime(enddatetime, "%Y-%m-%d %H:%M:%S.%f")

        dao = UsersDAO()
        unavailabilityid = dao.markTimeUnavailable(userid, startdatetime, enddatetime)
        if unavailabilityid:
            time_busy = (startdatetime, enddatetime, unavailabilityid)
            result = self.build_map_dict_unavailable(time_busy)
            return jsonify(result), 200
        else:
            return jsonify("NO RESULT"), 404

    # changed
    def markTimeAvailable(self, userid, json):#######################################################################
        #loggeduserid = json['loggeduserid']
        userunavailabilityid = json['userunavailabilityid']

        dao = UsersDAO()
        time_available = dao.markTimeAvailable(userid, userunavailabilityid)
        if time_available:
            result = self.build_map_dict_unavailable(time_available)
            return jsonify(result), 200
        else:
            return jsonify("NO RESULT"), 404


    # changed
    def allDaySchedule(self, userid, json):
        daystart = json['daystart']
        daystart = datetime.strptime(daystart, "%Y-%m-%d %H:%M:%S.%f")
        dayend = daystart + timedelta(days=1)
        dao = UsersDAO()
        sch_tuple, sch_unavailable = dao.allDaySchedule(userid, daystart, dayend)
        if not sch_tuple and not sch_unavailable:
            return jsonify("NO SCHEDULE"), 404
        else:
            result_list = []
            for appointment in sch_tuple:
                result = self.build_map_dict_schedule(appointment)
                result_list.append(result)
            for unavailability in sch_unavailable:
                tuple = (-1, "Unavailable Time Space", -1, unavailability[0], unavailability[1])
                result = self.build_map_dict_schedule(tuple)
                result_list.append(result)
            return jsonify(result_list), 200


    #statistics

    # changed
    def userWithMostReservation(self, userid):
        dao = UsersDAO()
        tuple = dao.userWithMostReservation(userid)
        if tuple:
            result = self.build_map_dict_mostreservations(tuple)
            return jsonify(result), 200
        else:
            return jsonify("NO RESULT FOUND."), 404

    def usersTopTen(self):
        dao = UsersDAO()
        tuples = dao.userTopTen()
        result = []
        if not tuples:
            return jsonify("NO RESULT FOUND."), 404
        else:
            for row in tuples:
                result.append(self.build_map_dict_mostreservations(row))
            return jsonify(result), 200

    def userMostUsedRoom(self, userid):
        dao = UsersDAO()
        tuple = dao.userMostUsedRoom(userid)
        if not tuple:
            return jsonify("NO RESULT FOUND."), 404
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
            result.append(self.build_map_dict_checkunavailable(item))

        return jsonify(result), 200



