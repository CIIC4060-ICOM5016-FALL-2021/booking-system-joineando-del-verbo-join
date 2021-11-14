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

    def allDayScheduleRoom(self, roomid):
        cursor = self.conn.cursor()
        query1 = "select reservationname, startdatetime, enddatetime " \
                  "from reservation " \
                  "where roomid = %s;"

        cursor.execute(query1, (roomid,))

        result = []
        for row in cursor:
            result.append(row)
        return result

    def whoAppointedRoom(self, roomid, time):
        cursor = self.conn.cursor()
        queryID = "select hostid " \
                 "from reservation " \
                 "where roomid = %s " \
                 "and startdatetime <= %s " \
                 "and enddatetime >= %s;"
        cursor.execute(queryID, (roomid, time, time,))
        hostid = cursor.fetchone()[0]
        query = "select firstname, lastname, userid " \
                "from users " \
                "where userid = %s;"
        cursor.execute(query, (hostid,))
        name = cursor.fetchone()
        return name

    def availableRoomAtTimeFrame(self, start, end):
        cursor = self.conn.cursor()
        queryavailable = "select roomid " \
                         "from room " \
                         "where roomid NOT IN (select roomid " \
                         "from roomunavailability);"
        cursor.execute(queryavailable)
        availables = cursor.rowcount
        print(availables)

        if availables > 0:
            roomid = cursor.fetchone()[0]


        else:
            queryID = "select roomid " \
                      "from roomunavailability " \
                      "where %s < startdatetime " \
                      "and %s > enddatetime;"
            cursor.execute(queryID, (end, start,))
            roomid = cursor.fetchone()[0]


        query = "select buildingname, roomnumber, roomtypename " \
                "from room natural inner join building natural inner join roomtype " \
                "where roomid = %s;"
        cursor.execute(query, (roomid,))
        room = cursor.fetchone()
        return room

    #statistics

    def roomTopTen(self):
        cursor = self.conn.cursor()
        query = "select t.roomid, t.buildingname, t.roomnumber " \
                "from (select roomid, buildingname, roomnumber, count(roomid) " \
                "from room natural inner join building natural inner join reservation " \
                "group by roomid, buildingname, roomnumber " \
                "order by count(roomid) desc, roomid) as t " \
                "limit 10;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result;






