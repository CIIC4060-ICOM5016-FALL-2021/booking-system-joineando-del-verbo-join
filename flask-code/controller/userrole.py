from flask import jsonify
from model.userrole import UserRoleDAO

class BaseUserRole:
    def build_map_dict(self, row):
        result = {}
        result['userroleid'] = row[0]
        result['userrolename'] = row[1]
        return result

    def addNewUserRole(self, json):
        userrolename = json["userrolename"]
        dao = UserRoleDAO()

        userroleid = dao.insertUserRole(userrolename)
        tuple = (userroleid, userrolename)
        result = self.build_map_dict(tuple)
        return jsonify(result), 200