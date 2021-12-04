from config.dbconfig import pg_config
import psycopg2

class UserRoleDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s port=%s host=%s" % (pg_config['database'], pg_config['user'],
                                                                                     pg_config['password'], pg_config['port'],
                                                                                     pg_config['host'])
        self.conn = psycopg2.connect(connection_url)

    def insertUserRole(self, userrolename):
        cursor = self.conn.cursor()
        query = "insert into userrole(userrolename) values (%s) returning userroleid;"
        cursor.execute(query, (userrolename,))
        userroleid = cursor.fetchone()[0]
        self.conn.commit()
        self.conn.close()
        return userroleid

    def getAllUserRoles(self):
        cursor = self.conn.cursor()
        query = "select userroleid, userrolename from userrole"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        self.conn.close()
        return result