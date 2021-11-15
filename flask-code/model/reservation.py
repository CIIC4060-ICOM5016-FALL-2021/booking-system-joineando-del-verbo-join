from config.dbconfig import pg_config
import psycopg2


class ReservationDAO:

    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s port=%s host=%s" % (pg_config['database'], pg_config['user'],
                                                                            pg_config['password'], pg_config['port'],
                                                                            pg_config['host'])
        self.conn = psycopg2.connect(connection_url)


    def createReservation(self, hostid, roomid, reservationname, startdatetime, enddatetime):

        cursor = self.conn.cursor()

        query = "insert into reservation(hostid, roomid, reservationname, startdatetime, enddatetime) \
                    values (%s, %s, %s, %s, %s) returning reservationid;"
        cursor.execute(query, (hostid, roomid, reservationname, startdatetime, enddatetime))
        reservationid = cursor.fetchone()[0]
        self.conn.commit()

        query2 = "insert into userunavailability(userid, startdatetime, enddatetime) values (%s, %s, %s);"
        cursor.execute(query2, (hostid, startdatetime, enddatetime))
        self.conn.commit()

        query3 = "insert into roomunavailability(roomid, startdatetime, enddatetime) values (%s, %s, %s);"
        cursor.execute(query3, (roomid, startdatetime, enddatetime))
        self.conn.commit()

        return reservationid


    def updateReservation(self, reservationid, hostid, roomid, reservationname, startdatetime, enddatetime):
        cursor = self.conn.cursor()

        # update userunavailability for host
        query1 = "select userunavailabilityid from userunavailability " \
                 "where userid=(select hostid from reservation where reservationid = %s) " \
                 "and startdatetime= (select startdatetime from reservation where reservationid = %s)" \
                 "and enddatetime= (select enddatetime from reservation where reservationid = %s);"
        cursor.execute(query1, (reservationid, reservationid, reservationid))
        userunavailabilityid = cursor.fetchone()

        query2 = "update userunavailability set userid= %s, startdatetime= %s, enddatetime= %s \
                            where userunavailabilityid =%s;"
        cursor.execute(query2, (hostid, startdatetime, enddatetime, userunavailabilityid))
        self.conn.commit()

        # update userunavailability for invitees
        query3 = "update userunavailability " \
                 "set startdatetime = %s, enddatetime = %s " \
                 "where startdatetime = (select startdatetime from reservation where reservationid = %s) " \
                 "and enddatetime = (select enddatetime from reservation where reservationid = %s) " \
                 "and userid IN (select inviteeid from invitation where reservationid =%s);"
        cursor.execute(query3, (startdatetime, enddatetime, reservationid, reservationid, reservationid))
        self.conn.commit()

        # update roomunavailability
        query4 = "select roomunavailabilityid from roomunavailability " \
                 "where roomid=(select roomid from reservation where reservationid = %s) " \
                 "and startdatetime=(select startdatetime from reservation where reservationid = %s) " \
                 "and enddatetime=(select enddatetime from reservation where reservationid = %s);"
        cursor.execute(query4, (reservationid, reservationid, reservationid))
        roomunavailabilityid = cursor.fetchone()

        query5 = "update roomunavailability set roomid= %s, startdatetime= %s, enddatetime= %s \
                            where roomunavailabilityid =%s;"
        cursor.execute(query5, (roomid, startdatetime, enddatetime, roomunavailabilityid))
        self.conn.commit()

        # update reservation
        query6 = "update reservation set hostid= %s, roomid= %s, reservationname= %s, startdatetime= %s, \
                            enddatetime= %s where reservationid=%s;"
        cursor.execute(query6, (hostid, roomid, reservationname, startdatetime, enddatetime, reservationid))
        self.conn.commit()

        affected_rows = cursor.rowcount

        return affected_rows == 1


    def deleteReservation(self, reservationid):
        cursor = self.conn.cursor()
        # could be subquery
        queryID = "select userunavailabilityid from userunavailability, reservation \
                    where reservation.hostid=userunavailability.userid \
                    and reservationid=%s \
                    and reservation.startdatetime=userunavailability.startdatetime \
                    and reservation.enddatetime=userunavailability.enddatetime;"
        cursor.execute(queryID, (reservationid,))
        userunavailabilityid = cursor.fetchone()

        query1 = "delete from userunavailability where userunavailabilityid=%s;"
        cursor.execute(query1, (userunavailabilityid,))
        self.conn.commit()

        #could be subquery
        queryID = "select roomunavailabilityid from roomunavailability, reservation \
                            where reservation.roomid=roomunavailability.roomid \
                            and reservationid=%s \
                            and reservation.startdatetime=roomunavailability.startdatetime \
                            and reservation.enddatetime=roomunavailability.enddatetime;"
        cursor.execute(queryID, (reservationid,))
        roomunavailabilityid = cursor.fetchone()

        query2 = "delete from roomunavailability where roomunavailabilityid=%s;"
        cursor.execute(query2, (roomunavailabilityid,))
        self.conn.commit()

        query3 = "delete from reservation where reservationid=%s;"
        cursor.execute(query3, (reservationid,))
        self.conn.commit()

        affected_rows = cursor.rowcount

        return affected_rows == 1


    def getReservationByID(self, reservationid):
        cursor = self.conn.cursor()
        query = "select reservationid, hostid, roomid, reservationname,\
         startdatetime, enddatetime from reservation where reservationid=%s;"
        cursor.execute(query, (reservationid,))
        result = cursor.fetchone()

        return result


    def didChangeTime(self, reservationid, startdatetime, enddatetime):
        cursor = self.conn.cursor()
        query = "select count(*) from reservation where reservationid=%s \
        and startdatetime=%s and enddatetime=%s;"
        cursor.execute(query, (reservationid,  startdatetime, enddatetime))
        count = cursor.fetchone()[0]

        return count == 0

    def allReservationsForRoom(self, roomid):
        cursor = self.conn.cursor()
        query = "select reservationid, hostid, roomid, reservationname, startdatetime, enddatetime " \
                "from reservation " \
                "where roomid = %s;"
        cursor.execute(query, (roomid,))
        result = []
        for row in cursor:
            result.append(row)
        self.conn.close()
        return result

    def busiestHours(self):
        cursor = self.conn.cursor()
        query = "select t.hours " \
                "from (select date_part('hour', startdatetime) as hours, count(date_part('hour', startdatetime)) as qty " \
                "from reservation " \
                "group by hours " \
                "order by qty desc, hours) as t " \
                "limit 5;"

        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        self.conn.close()
        return result

    def getRoomAppointments(self, roomid):
        cursor = self.conn.cursor()
        query = "select reservationID  , hostID , roomID , reservationName , startDateTime , " \
                "endDateTime from  reservation where reservation.roomid = %s;"
        cursor.execute(query, (roomid,))
        result = []
        for row in cursor:
           result.append(row)
        return result
