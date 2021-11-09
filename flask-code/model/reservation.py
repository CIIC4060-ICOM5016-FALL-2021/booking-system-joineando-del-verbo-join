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
        query = "insert into reservation(hostid, roomid, reservationname, startdatetime, enddatetime) values (%s, %s, %s, %s, %s) returning reservationid;"
        cursor.execute(query, (hostid, roomid, reservationname, startdatetime, enddatetime))
        reservationid = cursor.fetchone()[0]
        self.conn.commit()

        return reservationid


    def updateReservation(self, reservationid, hostid, roomid, reservationname, startdatetime, enddatetime):
        cursor = self.conn.cursor()
        query = "update reservation set hostid= %s, roomid= %s, reservationname= %s, startdatetime= %s, enddatetime= %s where reservationid=%s;"
        cursor.execute(query, (hostid, roomid, reservationname, startdatetime, enddatetime, reservationid))
        self.conn.commit()
        affected_rows = cursor.rowcount

        return affected_rows == 1


    def deleteReservation(self, reservationid):
        cursor = self.conn.cursor()
        query = "delete from reservation where reservationid=%s;"
        cursor.execute(query, (reservationid,))
        self.conn.commit()
        affected_rows = cursor.rowcount

        return affected_rows == 1


    def getReservationByID(self, reservationid):
        cursor = self.conn.cursor()
        query = "select reservationid, hostid, roomid, reservationname, startdatetime, enddatetime from reservation where reservationid=%s;"
        cursor.execute(query, (reservationid,))
        result = cursor.fetchone()
        return result


