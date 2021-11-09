from flask import jsonify
from model.building import BuildingDAO


class BaseBuilding:

    def build_map_dict(self, row):
        result = {}
        result['buildingid'] = row[0]
        result['buildingname'] = row[1]
        return result


    def addNewBuilding(self, json):
        buildingname = json["buildingname"]

        dao = BuildingDAO()

        buildingid = dao.insertBuilding(buildingname)
        result = self.build_map_dict((buildingid, buildingname))
        return jsonify(result), 200


    def updateBuilding(self, json, buildingid):
        buildingname = json["buildingname"]

        dao = BuildingDAO()

        updated = dao.updateBuilding(buildingid, buildingname)
        result = self.build_map_dict((buildingid, buildingname))
        if updated:
            return jsonify(result), 200
        else:
            return jsonify("NOT UPDATED"), 400


    def getBuildingByID(self, buildingid):
        dao = BuildingDAO()
        building = dao.getBuildingByID(buildingid)
        result = self.build_map_dict(building)
        if building:
            return jsonify(result), 200
        else:
            return jsonify("Not Found"), 404
