from config.dbconfig import pg_config
import psycopg2


class BuildingDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s port=%s host=%s" % (pg_config['database'], pg_config['user'],
                                                                            pg_config['password'], pg_config['port'],
                                                                            pg_config['host'])
        self.conn = psycopg2.connect(connection_url)


    def insertBuilding(self, buildingname):
        cursor = self.conn.cursor()
        query = "insert into building(buildingname) values (%s) returning buildingid;"
        cursor.execute(query, (buildingname,))
        buildingid = cursor.fetchone()[0]
        self.conn.commit()
        return buildingid


    def updateBuilding(self, buildingid, buildingname):
        cursor = self.conn.cursor()
        query = "update building set buildingname=%s where buildingid=%s;"
        cursor.execute(query, (buildingname, buildingid))
        self.conn.commit()
        affected_rows = cursor.rowcount
        return affected_rows == 1
