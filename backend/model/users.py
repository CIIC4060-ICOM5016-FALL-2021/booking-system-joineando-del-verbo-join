from config.dbconfig import pg_config
import psycopg2
from datetime import datetime


class UsersDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s port=%s host=%s" % (pg_config['database'], pg_config['user'],
                                                                                     pg_config['password'], pg_config['port'],
                                                                                     pg_config['host'])
        self.conn = psycopg2.connect(connection_url)


    def getAllUsers(self):
        cursor = self.conn.cursor()
        query = "select userid, firstname, lastname, email, password, roleid from users;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        self.conn.close()
        return result

    def validateEmail(self, email):
        cursor = self.conn.cursor()
        query = "select email from users where email = %s"
        cursor.execute(query, (email,))
        count = cursor.rowcount
        return True if (count == 0) else False


    def insertUser(self, firstname, lastname, email, password, roleid):
        cursor = self.conn.cursor()
        if not self.validateEmail(email):
            return -200
        query = "insert into users(firstname, lastname, email, password, roleid) values (%s, %s, %s, %s, %s) returning userid;"
        cursor.execute(query, (firstname, lastname, email, password, roleid))
        userid = cursor.fetchone()[0]
        self.conn.commit()
        self.conn.close()
        return userid


    def updateUser(self, firstname, lastname, email, password, roleid, userid):
        cursor = self.conn.cursor()
        query = "update users set firstname= %s, lastname= %s, email = %s, password= %s, roleid= %s where userid=%s;"
        cursor.execute(query, (firstname, lastname, email, password, roleid,userid))
        self.conn.commit()
        rows_updated = cursor.rowcount

        return rows_updated != 0


    def getUserByID(self, userid):
        cursor = self.conn.cursor()
        query = "select userid, firstname, lastname, email, password, roleid from users where userid = %s;"
        cursor.execute(query, (userid,))
        result = cursor.fetchone()

        return result


    def deleteUser(self, userid):
        cursor = self.conn.cursor()
        query = "delete from users where userid=%s;"
        cursor.execute(query, (userid,))
        affected_rows = cursor.rowcount
        self.conn.commit()
        self.conn.close()
        return affected_rows == 1

    #changed
    def checkUserAvailability(self, userid, startdatetime, enddatetime):
        cursor = self.conn.cursor()
        query = "select count(*) " \
                "from ((select startdatetime, enddatetime " \
                "from reservation where hostid = %s) " \
                "union all " \
                "(select startdatetime, enddatetime " \
                "from reservation natural inner join invitation " \
                "where inviteeid = %s) " \
                "union all " \
                "(select startdatetime, enddatetime " \
                "from userunavailability where userid = %s)) as t " \
                "where (%s >= t.startdatetime and %s <= t.enddatetime) " \
                "or (%s >= t.startdatetime and %s <= t.enddatetime) " \
                "or (%s <= t.startdatetime and %s >= t.enddatetime);"

        cursor.execute(query, (userid, userid, userid, startdatetime, startdatetime, enddatetime,
                               enddatetime, startdatetime, enddatetime))
        availability = cursor.fetchone()[0]

        return availability == 0

    # changed
    def markTimeUnavailable(self, userid, startdatetime, enddatetime):
        cursor = self.conn.cursor()
        query = "insert into userunavailability(userid, startdatetime, enddatetime) " \
                "values(%s, %s,%s) returning userunavailabilityid;"
        cursor.execute(query, (userid, startdatetime, enddatetime,))
        time_busy = cursor.fetchone()
        self.conn.commit()

        return time_busy

    def markTimeAvailable(self, userid, userunavailabilityid):
        cursor = self.conn.cursor()
        query = "delete from userunavailability " \
                "where userid = %s and userunavailabilityid = %s " \
                "returning startdatetime, enddatetime;"
        cursor.execute(query, (userid, userunavailabilityid,))
        time_available = cursor.fetchone()
        self.conn.commit()
        return time_available

    # changed - rethink
    def allDaySchedule(self, userid, startday, endday):
        cursor = self.conn.cursor()
        query1 = "(select reservationid, reservationname, roomid, startdatetime, enddatetime " \
                 "from reservation " \
                 "where hostid = %s and startdatetime >= %s and enddatetime <= %s) " \
                 "union all " \
                 "(select reservationid, reservationname, roomid, startdatetime, enddatetime " \
                 "from reservation natural inner join invitation " \
                 "where inviteeid = %s and startdatetime >= %s and enddatetime <= %s);"
        cursor.execute(query1, (userid, startday, endday, userid, startday, endday))
        result1 = []
        for row in cursor:
            result1.append(row)
        print(result1)

        query2 = "select startdatetime, enddatetime " \
                 "from userunavailability " \
                 "where userid = %s and startdatetime >= %s and enddatetime <= %s;"
        cursor.execute(query2, (userid, startday, endday))
        result2 = []
        for row in cursor:
            result2.append(row)
        print(result2)

        self.conn.close()

        return result1, result2

    def loginUser(self, email, password):
        cursor = self.conn.cursor()
        query = "select userid, firstname, lastname from users where email=%s and password=%s"
        cursor.execute(query, (email, password))
        result = cursor.fetchone()
        return result



    #statistics

    # changed
    def userWithMostReservation(self, userid):
        cursor = self.conn.cursor()
        query = "select u.userid, u.firstname, u.lastname, u.email, count(u.userid) as total " \
                "from users as u, " \
                "((select hostid as userid, reservationid from reservation) " \
                "union all " \
                "(select inviteeid as userid, reservationid from invitation)) as t " \
                "where u.userid = t.userid " \
                "and reservationid in " \
                "(select reservationid from reservation natural inner join invitation " \
                "where hostid = %s or inviteeid = %s) " \
                "and u.userid != %s " \
                "group by u.userid, u.firstname, u.lastname " \
                "order by total desc, u.userid;"
        cursor.execute(query, (userid,userid,userid))
        top_user = cursor.fetchone()
        self.conn.close()
        return top_user
        # result = []
        # for row in cursor:
        #     result.append(row)
        # return result

    def userTopTen(self):
        cursor = self.conn.cursor()
        query = "select userid, firstname, lastname, email, total " \
                "from users natural inner join (select userid, sum(quantity) as total " \
                "from ((select hostid as userid, count(hostid) as quantity " \
                "from reservation " \
                "group by hostid) " \
                "union all " \
                "(select inviteeid as userid, count(inviteeid) as quantity " \
                "from invitation " \
                "group by inviteeid)) as t1 " \
                "group by userid) as t2 " \
                "order by total desc, userid " \
                "limit 10;"
        cursor.execute(query)

        result = []
        for row in cursor:
            result.append(row)
        self.conn.close()
        return result


    def userMostUsedRoom(self, userid):
        cursor = self.conn.cursor()
        query = "select t.roomid, t.buildingname, t.roomnumber " \
                "from (select roomid, buildingname, roomnumber, count(roomid) " \
                "from room natural inner join building natural inner join reservation " \
                "where hostid = %s " \
                "group by roomid, buildingname, roomnumber " \
                "order by count(roomid) desc, roomid) as t;"
        cursor.execute(query, (userid,))
        result = cursor.fetchone()
        self.conn.close()
        return result

    # re-think this one
    def checkUnavailableOnTimeFrame(self, userid, startdatetime, enddatetime):
        cursor = self.conn.cursor()
        query = "select userid, startdatetime, endatetime " \
                "from ((select hostid as userid, startdatetime, enddatetime " \
                "from reservation where hostid = %s) " \
                "union all " \
                "(select inviteeid as userid, startdatetime, enddatetime " \
                "from reservation natural inner join invitation " \
                "where inviteeid = %s) " \
                "union all " \
                "(select userid, startdatetime, enddatetime " \
                "from userunavailability where userid = %s)) as t " \
                "where (%s >= t.startdatetime and %s <= t.enddatetime) " \
                "or (%s >= t.startdatetime and %s <= t.enddatetime) " \
                "or (%s <= t.startdatetime and %s >= t.enddatetime);"
        cursor.execute(query, (userid, userid, userid, startdatetime, startdatetime, enddatetime,
                               enddatetime, startdatetime, enddatetime))
        result = []
        for row in cursor:
            result.append(row)

        return result






