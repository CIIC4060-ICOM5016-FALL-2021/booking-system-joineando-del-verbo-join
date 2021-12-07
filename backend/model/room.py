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
        self.conn.close()
        return roomid

    def getAllRooms(self):
        cursor = self.conn.cursor()
        query = "select roomid, roomnumber, roomcapacity, buildingid, buildingname, typeid from room natural inner join building;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        self.conn.close()
        return result

    def getRoomById(self, roomid):
        cursor = self.conn.cursor()
        query = "select roomid, roomnumber, roomcapacity, buildingid, buildingname, typeid " \
                "from room natural inner join building where roomid=%s;"
        cursor.execute(query, (roomid,))
        result = cursor.fetchone()
        self.conn.close()
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
        self.conn.close()
        return rows_deleted != 0

    # changed
    def allDayScheduleRoom(self, roomid, startday, endday):
        cursor = self.conn.cursor()
        query1 = "select hostid, reservationid, reservationname, startdatetime, enddatetime , firstname, lastname " \
                 "from reservation  inner join users on(users.userid = reservation.hostid)" \
                 "where roomid = %s and startdatetime >= %s and enddatetime <= %s;"
        cursor.execute(query1, (roomid, startday, endday,))
        result1 = []
        for row in cursor:
            result1.append(row)

        query2 = "select startdatetime, enddatetime " \
                 "from roomunavailability  " \
                 "where roomid = %s and startdatetime >= %s and enddatetime <= %s;"
        cursor.execute(query2, (roomid, startday, endday,))
        result2 = []
        for row in cursor:
            result2.append(row)
        self.conn.close()

        return result1, result2

    def whoAppointedRoom(self, roomid, time):
        cursor = self.conn.cursor()

        queryID = "select hostid " \
                 "from reservation " \
                 "where roomid = %s " \
                 "and startdatetime <= %s " \
                 "and enddatetime >= %s;"
        cursor.execute(queryID, (roomid, time, time,))
        if not cursor.fetchone():
            return
        hostid = list(cursor.fetchone())[0]

        query = "select firstname, lastname, userid " \
                "from users " \
                "where userid = %s;"

        cursor.execute(query, (hostid,))
        name = cursor.fetchone()
        self.conn.close()
        return name

    # change
    def availableRoomAtTimeFrame(self, start, end):
        cursor = self.conn.cursor()
        queryavailable = "select distinct roomid, buildingname, roomnumber, roomtypename " \
                         "from room natural inner join building, roomtype " \
                         "where typeid = roomtypeid " \
                         "and roomid NOT IN (select distinct t.roomid " \
                         "from ((select roomid, startdatetime, enddatetime from reservation) " \
                         "union all " \
                         "(select roomid, startdatetime, enddatetime from roomunavailability)) as t " \
                         "where (%s >= t.startdatetime and %s < t.enddatetime) " \
                         "or (%s > t.startdatetime and %s <= t.enddatetime) " \
                         "or (%s <= t.startdatetime and %s >= t.enddatetime));"
        cursor.execute(queryavailable, (start, start, end, end, start, end))

        rooms = []
        for room in cursor:
            rooms.append(room)
        self.conn.close()
        return rooms

    #statistics

    # changed
    def roomTopTen(self):
        cursor = self.conn.cursor()
        query = "select t.roomid, t.buildingname, t.roomnumber, quantity " \
                "from (select roomid, buildingname, roomnumber, count(roomid) as quantity " \
                "from room natural inner join building natural inner join reservation " \
                "group by roomid, buildingname, roomnumber " \
                "order by quantity desc, roomid) as t " \
                "limit 10;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        self.conn.close()
        return result

    # changed
    def checkRoomAvailability(self, roomid, startdatetime, enddatetime):
        cursor = self.conn.cursor()
        query = "select count(*) " \
                "from ((select startdatetime, enddatetime " \
                "from reservation where roomid = %s) " \
                "union all " \
                "(select startdatetime, enddatetime " \
                "from roomunavailability where roomid = %s)) as t " \
                "where (%s >= t.startdatetime and %s < t.enddatetime) " \
                "or (%s > t.startdatetime and %s <= t.enddatetime) " \
                "or (%s <= t.startdatetime and %s >= t.enddatetime);"

        cursor.execute(query, (roomid, roomid, startdatetime, startdatetime, enddatetime,
                               enddatetime, startdatetime, enddatetime))
        availability = cursor.fetchone()[0]


        return availability == 0

    def makeRoomUnavailable(self, roomid, startdatetime, enddatetime):
        cursor = self.conn.cursor()
        query = "insert into roomunavailability(roomid, startdatetime, enddatetime) values (%s, %s, %s) " \
                "returning roomunavailabilityid;"
        cursor.execute(query, (roomid,startdatetime, enddatetime))
        roomunavailabilityid = cursor.fetchone()[0]
        self.conn.commit()

        return roomunavailabilityid

    # changed
    def makeRoomAvailable(self, roomunavailabilityid):
        cursor = self.conn.cursor()
        query = "delete from roomunavailability where roomunavailabilityid = %s;"
        cursor.execute(query, (roomunavailabilityid,))
        rows_deleted = cursor.rowcount
        self.conn.commit()

        return rows_deleted != 0


    def getAllRoomUnavailableSlot(self, roomid):
        cursor = self.conn.cursor()
        query = "select startdatetime, enddatetime, roomunavailabilityid " \
                "from roomunavailability " \
                "where roomid = %s;"
        cursor.execute(query, (roomid,))
        result = []
        for row in cursor:
            result.append(row)

        return result

    def getAllBuildings(self):
        cursor = self.conn.cursor()
        query = "select buildingid, buildingname from building;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        self.conn.close()
        return result

    def getAllRoomTypes(self):
        cursor = self.conn.cursor()
        query = "select roomtypeid, roomtypename from roomtype;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        self.conn.close()
        return result










