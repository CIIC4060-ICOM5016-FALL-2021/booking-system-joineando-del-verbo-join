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

    def getAllUserRoles(self):
        dao = UserRoleDAO()
        role_tuples = dao.getAllUserRoles()
        result_list = []
        if not role_tuples:
            dao.conn.close()
            return jsonify("NOT FOUND"), 404
        else:
            for role in role_tuples:
                result = self.build_map_dict(role)
                result_list.append(result)
            dao.conn.close()
            return jsonify(result_list), 200


    def getUserRolesByID(self, userroleid):
        dao = UserRoleDAO()
        role = dao.getUserRolesbyID(userroleid)
        if role:
            dao.conn.close()
            result = self.build_map_dict(role)
            return jsonify(result), 200
        else:
            dao.conn.close()
            return jsonify("NOT FOUND"), 404




