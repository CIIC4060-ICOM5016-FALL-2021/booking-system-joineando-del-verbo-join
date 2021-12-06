from flask import jsonify
from model.room import RoomDAO
from model.users import UsersDAO
from datetime import datetime, timedelta
from model.reservation import ReservationDAO
from controller.reservation import BaseReservation
from model.users import UsersDAO


class BaseRoom:

    # data formatter (list -> dict)
    def build_map_dict(self, row):
        result = {}
        result['roomid'] = row[0]
        result['roomnumber'] = row[1]
        result['roomcapacity'] = row[2]
        result['buildingid'] = row[3]
        result['typeid'] = row[4]
        return result

    def build_map_dict_all(self, row):
        result = {}
        result['roomid'] = row[0]
        result['roomnumber'] = row[1]
        result['roomcapacity'] = row[2]
        result['buildingid'] = row[3]
        result['buildingname'] = row[4]
        result['typeid'] = row[5]
        return result

    def build_map_dict_schedule(self, row):
        result = {}
        result['hostid'] = row[0]
        result['reservationid'] = row[1]
        result['reservationname'] = row[2]
        result['startdatetime'] = row[3]
        result['enddatetime'] = row[4]
        return result

    def build_map_dict_name(self, row: tuple):
        result = {}
        result['firstname'] = row[0]
        result['lastname'] = row[1]
        result['userid'] = row[2]
        return result

    def build_map_dict_roomavailable(self, row):
        result = {}
        result['buildingname'] = row[0]
        result['roomnumber'] = row[1]
        result['roomtypename'] = row[2]
        return result

    def build_map_dict_roomunavailable(self, row):
        result={}
        result['roomunavailabilityid'] = row[0]
        result['roomid'] = row[1]
        result['startdatetime'] = row[2]
        result['enddatetime'] = row[3]
        return result

    # changed
    def build_map_dict_mostreserved(self, row):
        result = {}
        result['roomid'] = row[0]
        result['buildingname'] = row[1]
        result['roomnumber'] = row[2]
        result['reservations'] = row[3]
        return result

    def build_map_dict_unavailable(self, row):
        result = {}
        result['startdatetime'] = row[0]
        result['enddatetime'] = row[1]
        result['roomunavailabilityid'] = row[2]
        return result


    # methods
    def addNewRoom(self, json):
        roomnumber = json["roomnumber"]
        roomcapacity = json["roomcapacity"]
        buildingid = json["buildingid"]
        typeid = json["typeid"]
        dao = RoomDAO()
        roomid = dao.insertRoom(roomnumber, roomcapacity, buildingid, typeid)
        if roomid:
            room_tuple = (roomid, roomnumber, roomcapacity, buildingid, typeid)
            result = self.build_map_dict(room_tuple)
            return jsonify(result), 200
        else:
            return jsonify("NOT CREATED"), 400

    # verified
    def getAllRooms(self):
        dao = RoomDAO()
        room_list = dao.getAllRooms()
        result_list = []
        for row in room_list:
            obj = self.build_map_dict_all(row)
            result_list.append(obj)
        return jsonify(result_list), 200

    # verified
    def getRoomByID(self, roomid):
        dao = RoomDAO()
        room_tuple = dao.getRoomById(roomid)
        if room_tuple:
            result = self.build_map_dict(room_tuple)
            return jsonify(result), 200
        else:
            return jsonify("ROOM NOT FOUND"), 404

    # verified
    def updateRoom(self, json, roomid):
        roomnumber = json["roomnumber"]
        roomcapacity = json["roomcapacity"]
        buildingid = json["buildingid"]
        typeid = json["typeid"]
        dao = RoomDAO()
        code_updated = dao.updateRoom(roomid, roomnumber, roomcapacity, buildingid, typeid)
        if code_updated:
            room_tuple = (roomid, roomnumber, roomcapacity, buildingid, typeid)
            result = self.build_map_dict(room_tuple)
            return jsonify(result), 200
        else:
            return jsonify("ROOM NOT FOUND"), 404

    def deleteRoom(self, roomid):
        dao = ReservationDAO()
        room_reservations = dao.allReservationsForRoom(roomid)
        for res in room_reservations:
            BaseReservation().deleteReservation(res[0])

        dao = RoomDAO()
        result = dao.deleteRoom(roomid)
        if result:
            return jsonify("ROOM DELETED"), 200
        else:
            return jsonify("ROOM NOT FOUND"), 404

    # changed
    def allDayScheduleRoom(self, roomid, json):
        userid = json['userid']
        daystart = json['daystart']
        daystart = datetime.strptime(daystart, "%Y-%m-%d %H:%M:%S.%f")
        dayend = daystart + timedelta(days=1)

        usersDAO = UsersDAO()
        userInfo = usersDAO.getUserByID(userid)
        if userInfo:
            userRoleID = userInfo[5]
        else:
            userRoleID = -1

        if userRoleID == 3:
            dao = RoomDAO()
            schedule, sch_unavailable = dao.allDayScheduleRoom(roomid, daystart, dayend)
            if not schedule and not sch_unavailable:
                return jsonify("NO SCHEDULE"), 404
            else:
                result_list = []
                for row in schedule:
                    obj = self.build_map_dict_schedule(row)
                    result_list.append(obj)
                for row in sch_unavailable:
                    tuple = (-1, -1, "Unavailable Time Space", row[0], row[1])
                    obj = self.build_map_dict_schedule(tuple)
                    result_list.append(obj)
                return jsonify(result_list), 200
        else:
            return jsonify("ACCESS DENIED"), 403

    def whoAppointedRoom(self, roomid, json):
        time = json['time']
        time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S.%f")
        dao = RoomDAO()
        name = dao.whoAppointedRoom(roomid, time)
        if name:
            result = self.build_map_dict_name(name)
            return jsonify(result), 200
        else:
            return("NOT FOUND"), 404

    def availableRoomAtTimeFrame(self, json):
        start = json['startdatetime']
        end = json['enddatetime']
        start = datetime.strptime(start, "%Y-%m-%d %H:%M:%S.%f")
        end = datetime.strptime(end, "%Y-%m-%d %H:%M:%S.%f")
        dao = RoomDAO()
        room = dao.availableRoomAtTimeFrame(start, end)
        result = self.build_map_dict_roomavailable(room)
        return jsonify(result), 200

    #statistics

    def roomTopTen(self):
        dao = RoomDAO()
        tuples = dao.roomTopTen()
        result = []
        for row in tuples:
            result.append(self.build_map_dict_mostreserved(row))
        return jsonify(result), 200

    def makeRoomUnavailable(self, roomid, json):
        userid = json['userid']
        start = json['startdatetime']
        end = json['enddatetime']
        start = datetime.strptime(start, "%Y-%m-%d %H:%M:%S.%f")
        end = datetime.strptime(end, "%Y-%m-%d %H:%M:%S.%f")

        if start > end:
            return jsonify("END TIME SHOULD BE AFTER START TIME"), 400

        usersDAO = UsersDAO()
        userInfo = usersDAO.getUserByID(userid)
        if userInfo:
            userRoleID = userInfo[5]
        else:
            userRoleID = -1

        if userRoleID == 3:
            roomDAO = RoomDAO()
            roomunavailabilityid = roomDAO.makeRoomUnavailable(roomid, start, end)
            tuple = (roomunavailabilityid, roomid, start, end)
            result = self.build_map_dict_roomunavailable(tuple)
            return jsonify(result), 200
        else:
            return jsonify("ACCESS DENIED"), 403

    def makeRoomAvailable(self, json):
        userid = json['userid']
        roomunavailabilityid = json["roomunavailabilityid"]

        usersDAO = UsersDAO()
        userInfo = usersDAO.getUserByID(userid)
        if userInfo:
            userRoleID = userInfo[5]

        else:
            userRoleID = -1
        print("Here: ",userRoleID)
        if userRoleID == 3:
            roomDAO = RoomDAO()
            is_deleted = roomDAO.makeRoomAvailable(roomunavailabilityid)
            if is_deleted:
                return jsonify("ROOM WAS MADE AVAILABLE"), 200
            else:
                return jsonify("ROOM WAS ALREADY AVAILABLE"), 404
        else:
            return jsonify("ACCESS DENIED"), 403


    def getAllRoomUnavailableSlot(self, roomid):
        dao = RoomDAO()
        result = dao.getAllRoomUnavailableSlot(roomid)
        if not result:
            return jsonify("NO UNAVAILABILITY"), 404
        else:
            result_list = []
            for slot in result:
                element = self.build_map_dict_unavailable(slot)
                result_list.append(element)
            return jsonify(result_list), 200
