from config.dbconfig import pg_config
import psycopg2


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
        return result


    def insertUser(self, firstname, lastname, email, password, roleid):
        cursor = self.conn.cursor()
        query = "insert into users(firstname, lastname, email, password, roleid) values (%s, %s, %s, %s, %s) returning userid;"
        cursor.execute(query, (firstname, lastname, email, password, roleid))
        userid = cursor.fetchone()[0]
        self.conn.commit()
        return userid


    def updateUser(self, firstname, lastname, email, password, roleid, userid):
        cursor = self.conn.cursor()
        query = "update users set firstname= %s, lastname= %s, email = %s, password= %s, roleid= %s where userid=%s;"
        cursor.execute(query, (firstname, lastname, email, password, roleid,userid))
        self.conn.commit()
        return True


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
        return affected_rows == 1


    def checkUserAvailability(self, userid, startdatetime, enddatetime):
        cursor = self.conn.cursor()
        query = "select count(*) from userunavailability \
               where userunavailability.userid = %s \
               and ((%s >= userunavailability.startdatetime \
               and %s <= userunavailability.enddatetime) \
               or (%s >= userunavailability.startdatetime \
               and %s<= userunavailability.enddatetime) \
               or (%s <= userunavailability.startdatetime \
               and %s >= userunavailability.enddatetime ));"

        cursor.execute(query, (userid, startdatetime, startdatetime, enddatetime,
                               enddatetime, startdatetime, enddatetime))
        availability = cursor.fetchone()[0]

        return availability == 0

    # def allDayScheduleUser(self, userid):
    #     cursor = self.conn.cursor()
    #     query = "select reservationname, startdatetime, enddatetime " \
    #             "from "







