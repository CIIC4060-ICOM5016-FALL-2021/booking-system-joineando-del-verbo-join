from config.dbconfig import pg_config
import psycopg2

class RoomDAO:

    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s port=%s host=%s" % (pg_config['database'], pg_config['user'],
                                                                        pg_config['password'], pg_config['port'],
                                                                        pg_config['host'])
        self.conn = psycopg2.connect(connection_url)

    def insertRoom(self, roomnumber, roomcapacity, buildingid, typeid):
        cursor = self.conn.cursor()
        query = "insert into room(roomnumber, roomcapacity, buildingid, typeid) values (%s, %s, %s, %s) returning roomid"
        cursor.execute(query, (roomnumber, roomcapacity, buildingid, typeid))
        roomid = cursor.fetchone()[0]
        self.conn.commit()
        return roomid

    def getAllRooms(self):
        cursor = self.conn.cursor()
        query = "select roomid, roomnumber, roomcapacity, buildingid, typeid from room;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getRoomById(self, roomid):
        cursor = self.conn.cursor()
        query = "select roomid, roomnumber, roomcapacity, buildingid, typeid from room where roomid=%s;"
        cursor.execute(query, (roomid,))
        result = cursor.fetchone()
        return result

    def updateRoom(self, roomid, roomnumber, roomcapacity, buildingid, typeid):
        cursor = self.conn.cursor()
        query = "update room set roomnumber=%s, roomcapacity=%s, buildingid=%s, typeid=%s where roomid=%s;"
        cursor.execute(query, (roomnumber, roomcapacity, buildingid, typeid, roomid))
        rows_updated = cursor.rowcount
        self.conn.commit()
        return rows_updated != 0

    def deleteRoom(self, roomid):
        cursor = self.conn.cursor()
        query = "delete from room where roomid=%s"
        cursor.execute(query, (roomid,))
        rows_deleted = cursor.rowcount
        self.conn.commit()
        return rows_deleted != 0

