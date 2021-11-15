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
        query1 = "insert into invitation(inviteeid, reservationid) values(%s,%s);"
        cursor.execute(query1, (userid,reservationid,))
        self.conn.commit()

        query2 = "select startdatetime, enddatetime " \
                 "from reservation " \
                 "where reservationid = %s;"
        cursor.execute(query2, (reservationid,))
        result = cursor.fetchone()
        startdatetime = result[0]
        enddatetime = result[1]

        query3 = "insert into userunavailability(userid, startdatetime, enddatetime) " \
                 "values (%s, %s, %s);"
        cursor.execute(query3, (userid, startdatetime, enddatetime,))
        self.conn.commit()

        query4 = "select hostid, inviteeid, reservationid, reservationname, startdatetime, enddatetime, roomid " \
                 "from reservation natural inner join invitation " \
                 "where reservationid = %s and inviteeid = %s;"
        cursor.execute(query4, (reservationid, userid))
        confirmation = cursor.fetchone()
        self.conn.close()
        return confirmation

    def getInvitationByID(self, reservationid, inviteeid):
        cursor = self.conn.cursor()
        query = "select hostid, inviteeid, reservationid, reservationname, startdatetime, enddatetime, roomid " \
                "from invitation natural inner join reservation " \
                "where invitation.reservationid=%s and invitation.inviteeid=%s;"
        cursor.execute(query, (reservationid, inviteeid))
        invitation = cursor.fetchone()
        self.conn.close()
        return invitation


    def allInviteesForReservation(self, reservationid):
        cursor = self.conn.cursor()
        query = "select userid, firstname, lastname " \
                "from users inner join invitation ON users.userid=invitation.inviteeid " \
                "where reservationid = %s;"
        cursor.execute(query, (reservationid,))
        result = []
        for row in cursor:
            result.append(row)
        self.conn.close()
        return result


    def updateInvitation(self, reservationid, startdatetime, enddatetime):
        cursor = self.conn.cursor()

        query = "update userunavailability " \
                "set startdatetime = %s, enddatetime = %s " \
                "where startdatetime = (select startdatetime from reservation where reservationid = %s) " \
                "and enddatetime = (select enddatetime from reservation where reservationid = %s) " \
                "and userid IN (select inviteeid from invitation where reservationid =%s);"
        cursor.execute(query, (startdatetime, enddatetime, reservationid, reservationid,reservationid ))
        self.conn.commit()
        affectedrows = cursor.rowcount
        self.conn.close()
        return affectedrows != 0


    def deleteInvitation(self, userid, reservationid):
        cursor = self.conn.cursor()
        query = "delete from invitation where inviteeid = %s and reservationid = %s;"
        cursor.execute(query,(userid, reservationid,))
        self.conn.commit()
        affectedrows = cursor.rowcount

        query2 = "delete from userunavailability " \
                 "where startdatetime = (select startdatetime from reservation where reservationid = %s) " \
                 "and enddatetime = (select enddatetime from reservation where reservationid = %s)" \
                 "and userid=%s;"
        cursor.execute(query2, (reservationid, reservationid, userid))
        self.conn.commit()

        self.conn.close()
        return affectedrows !=0

