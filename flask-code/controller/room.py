from flask import jsonify
from model.room import RoomDAO

class BaseRoom:

    def build_map_dict(self, row):
        result = {}
        result['roomid'] = row[0]
        result['roomnumber'] = row[1]
        result['roomcapacity'] = row[2]
        result['buildingid'] = row[3]
        result['typrid'] = row[4]
        return result

    def getAllRooms(self):
        dao = RoomDAO()
        room_list = dao.getAllRooms()
        result_list = []
        for row in room_list:
            obj = self.build_map_dict(row)
            result_list.append(obj)
        return jsonify(result_list)

    def getRoomById(self, roomid):
        dao = RoomDAO()
        tuple = dao.getRoomById(roomid)
        if not tuple:
            return jsonify("Not Found"), 404
        else:
            result = self.build_map_dict(tuple)
            return jsonify(result), 200

    def addNewRoom(self, json):
        roomnumber = json['roomnumber']
        roomcapacity = json['roomcapacity']
        buildingid = json['buildingid']
        typeid = json['typeid']
        dao = RoomDAO()
        roomid = dao.insertRoom(roomnumber, roomcapacity, buildingid, typeid)
        tuple = (roomid, roomnumber, roomcapacity, buildingid, typeid)
        result = self.build_map_dict(tuple)
        return jsonify(result), 201

    def updateRoom(self, json):
        roomnumber = json['roomnumber']
        roomcapacity = json['roomcapacity']
        buildingid = json['buildingid']
        typeid = json['typeid']
        roomid = json['roomid']
        dao = RoomDAO()
        updated_code = dao.updateRoom(roomid, roomnumber, roomcapacity, buildingid, typeid)
        tuple = (roomid, roomnumber, roomcapacity, buildingid, typeid)
        result = self.build_map_dict(tuple)
        return jsonify(result), 200

    def deleteRoom(self, roomid):
        dao = RoomDAO()
        result = dao.deleteRoom(roomid)
        if result:
            return jsonify("DELETED"), 200
        else:
            return jsonify("NOT FOUND"), 404