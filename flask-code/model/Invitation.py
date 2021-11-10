from config.dbconfig import pg_config
import psycopg2

class InvitationDAO:

    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s port=%s host=%s" % (pg_config['database'], pg_config['user'],
                                                                            pg_config['password'], pg_config['port'],
                                                                            pg_config['host'])
        self.conn = psycopg2.connect(connection_url)

    def createInvitation(self, userid, reservationid):
        cursor = self.conn.cursor()

        query1 = "insert into invitation(userid, reservationid) values(%s,%s)"
        cursor.execute(query1, (userid,reservationid,))
        self.conn.commit()

        # query2 = "insert into userunavailability(userid, startdatetime, enddatetime) values (%s, %s, %s);"
        # cursor.execute(query2, (userid, startdatetime, enddatetime))
        # userunavailabilityid = cursor.fetchone()[0]
        # self.conn.commit()


        return True

    def allInviteesForReservation(self, reservationid):
        cursor = self.conn.cursor()
        query = "select userid, firstname, lastname, reservationname " \
                "from users natural inner join reservation natural inner join invitation " \
                "where reservationid = %s;"
        cursor.execute(query, (reservationid,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def updateInvitation(self, userid, reservationid):
        cursor = self.conn.cursor()
        query = "update invitation set userid = %s where reservationid = %s;"
        cursor.execute(query,(userid, reservationid,))
        self.conn.commit()
        return True

    def deleteInvitation(self, userid, reservationid):
        cursor = self.conn.cursor()
        query = "delete from invitation where userid = %s and reservationid = %s;"
        cursor.execute(query,(userid, reservationid,))
        self.conn.commit()

        query2 = "delete from userunavailability "

        affectedrows = cursor.rowcount

        return affectedrows == 1
