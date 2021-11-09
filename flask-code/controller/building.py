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