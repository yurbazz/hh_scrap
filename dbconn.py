import pymysql.cursors

mysql_conn = pymysql.connect(host='localhost',
                             user='jobsdb',
                             password='password',
                             db='JobsDB',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.Cursor)

title = 'Инженер ИТ / IT Engineer'
company = 'Tieto'

mysql_cursor = mysql_conn.cursor()

sql = "SELECT title FROM `titles` WHERE `title` = %s"
if mysql_cursor.execute(sql, title) == 0:
    sql = "INSERT INTO `titles` (`title`,`type`) VALUES (%s,%s)"
    mysql_cursor.execute(sql, (title, '1'))
    mysql_conn.commit()

sql = "SELECT company FROM `companys` WHERE `company` = %s"
if mysql_cursor.execute(sql, company) == 0:
    sql = "INSERT INTO `companys` (`company`) VALUES (%s)"
    mysql_cursor.execute(sql, company)
    mysql_conn.commit()

mysql_conn.close()
