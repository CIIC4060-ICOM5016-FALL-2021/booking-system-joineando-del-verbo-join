from flask import jsonify
from model.room import RoomDAO


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

    # methods
    def addNewRoom(self, json):
        roomnumber = json["roomnumber"]
        roomcapacity = json["roomcapacity"]
        buildingid = json["buildingid"]
        typeid = json["typeid"]
        dao = RoomDAO()
        roomid = dao.insertRoom(roomnumber, roomcapacity, buildingid, typeid)
        tuple = (roomid, roomnumber, roomcapacity, buildingid, typeid)
        result = self.build_map_dict(tuple)
        return jsonify(result), 201

    def getAllRooms(self):
        dao = RoomDAO()
        room_list = dao.getAllRooms()
        result_list = []
        for row in room_list:
            obj = self.build_map_dict(row)
            result_list.append(obj)
        return jsonify(result_list), 200

    def getRoomByID(self, roomid):
        dao = RoomDAO()
        tuple = dao.getRoomById(roomid)
        if tuple:
            result = self.build_map_dict(tuple)
            return jsonify(result), 200
        else:
            return jsonify("Room Not Found."), 404

    def updateRoom(self, json, roomid):
        roomnumber = json["roomnumber"]
        roomcapacity = json["roomcapacity"]
        buildingid = json["buildingid"]
        typeid = json["typeid"]
        dao = RoomDAO()
        code_updated = dao.updateRoom(roomid, roomnumber, roomcapacity, buildingid, typeid)
        if code_updated:
            tuple = (roomid, roomnumber, roomcapacity, buildingid, typeid)
            result = self.build_map_dict(tuple)
            return jsonify(result), 200
        else:
            return jsonify("Room Not Found."), 404

    def deleteRoom(self, roomid):
        dao = RoomDAO()
        result = dao.deleteRoom(roomid)
        if result:
            return jsonify("Room Deleted."), 200
        else:
            return jsonify("Room Not Found."), 404

    def allDayScheduleRoom(self, roomid):
        dao = RoomDAO()
        schedules = dao.allDayScheduleRoom(roomid)
        result_list = []
        for row in schedules:
            obj = self.build_map_dict_unaivalaible(row)
            result_list.append(obj)
        return jsonify(result_list), 200

