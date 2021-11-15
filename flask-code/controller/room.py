from flask import jsonify
from model.room import RoomDAO
from datetime import datetime


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

    def build_map_dict_unaivalaible(self, row):
        result = {}
        result['reservationname'] = row[0]
        result['startdatetime'] = row[1]
        result['enddatetime'] = row[2]
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


    def build_map_dict_mostreserved(self, row):
        result = {}
        result['roomid'] = row[0]
        result['buildingname'] = row[1]
        result['roomnumber'] = row[2]
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
            obj = self.build_map_dict(row)
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
        dao = RoomDAO()
        result = dao.deleteRoom(roomid)
        if result:
            return jsonify("ROOM DELETED"), 200
        else:
            return jsonify("ROOM NOT FOUND"), 404

    def allDayScheduleRoom(self, roomid):
        dao = RoomDAO()
        schedules = dao.allDayScheduleRoom(roomid)
        result_list = []
        for row in schedules:
            obj = self.build_map_dict_unaivalaible(row)
            result_list.append(obj)
        return jsonify(result_list), 200

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




