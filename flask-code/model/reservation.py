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