import pymysql.cursors

job_dict = {}
job_dict['title'] = 'Инженер ИТ / IT Engineer'
job_dict['company'] = 'Tieto'
job_dict['id'] = '25110626'
job_dict['url'] = 'https://krasnodar.hh.ru/vacancy/25110626'
job_dict['date'] = '2018-04-29 00:00:00'
job_dict['promo'] = 0
job_dict['salary'] = '50 000-60 000 руб.'
job_dict['responsibility'] = 'Управление и разрешение сетевых инцидентов и запросов на обслуживание в производственной ' \
                 'инфраструктуре. Решение сетевых проблем, связанных с компьютерами, управляющим производственными...'
job_dict['requirement'] = 'Профильное высшее образование (ИТ, телекоммуникации). Разговорный и письменный английский язык, ' \
              'знание технической терминологии. Опыт системного администрирования - не менее 2 лет.'


mysql_conn = pymysql.connect(host='localhost',
                             user='jobsdb',
                             password='password',
                             db='JobsDB',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.Cursor)

cur = mysql_conn.cursor()


def new_insert(job_dict):
    sql = "SELECT title FROM `titles` WHERE `title` = %s"
    if cur.execute(sql, job_dict['title']) == 0:
        sql = "INSERT INTO `titles` (`title`,`type`) VALUES (%s,%s)"
        cur.execute(sql, (job_dict['title'], '1'))
        mysql_conn.commit()
    sql = "SELECT id FROM `titles` WHERE `title` = %s"
    cur.execute(sql, job_dict['title'])
    job_dict['title_id'] = int(cur.fetchone()[0])

    sql = "SELECT company FROM `companys` WHERE `company` = %s"
    if cur.execute(sql, job_dict['company']) == 0:
        sql = "INSERT INTO `companys` (`company`) VALUES (%s)"
        cur.execute(sql, job_dict['company'])
        mysql_conn.commit()
    sql = "SELECT id FROM `companys` WHERE `company` = %s"
    cur.execute(sql, job_dict['company'])
    job_dict['company_id'] = int(cur.fetchone()[0])

    sql = "INSERT INTO `jobs_info` " \
          "     (`job_id`, `title_id`, `company_id`, `p_date`, `u_date`, `salary`, `url`, `responsibility`, " \
          "     `requirement`, `promo`, `updates`) " \
          "VALUES (%(id)s, %(title_id)s, %(company_id)s, %(date)s, %(date)s, %(salary)s, %(url)s, " \
          "        %(responsibility)s, %(requirement)s, %(promo)s, 0)"
    cur.execute(sql, job_dict)
    mysql_conn.commit()


# Skip if vacancy is not interesting
sql = "SELECT type FROM `titles` WHERE `title` = %s"
cur.execute(sql, job_dict['title'])
if cur.fetchone()[0] == 2:
    print("Exclude, go to next vacancy")
    mysql_conn.close()
    exit()

# Check if we get all new vacancies and can stop...
sql = "SELECT 1 FROM `jobs_info` WHERE `job_id` = %s AND `u_date` = %s"
if cur.execute(sql, (job_dict['id'], job_dict['date'])) == 1:
    # ...But not if old vacancy is in promo list
    sql = "SELECT promo FROM `jobs_info` WHERE `job_id` = %s"
    cur.execute(sql, job_dict['id'])
    if cur.fetchone() == 1:
        print("It's a promo, go to next vacancy")
        mysql_conn.close()
        exit()
    else:
        print("Stop processing")
        mysql_conn.close()
        exit()

# Check if vacancy is exist and confirmed on new date
sql = "SELECT 1 FROM `jobs_info` WHERE `job_id` = %s AND `title_id` = (SELECT id FROM `titles` WHERE `title` = %s)"
if cur.execute(sql,(job_dict['id'],job_dict['title'])) == 1:
    # Update date of confirmation
    sql = "UPDATE `jobs_info` SET `u_date` = %s, `updates` = `updates` + 1 WHERE `job_id` = %s"
    cur.execute(sql, (job_dict['date'],job_dict['id']))
    mysql_conn.commit()
    print("Date updated, go to next vacancy")
    mysql_conn.close()
    exit()
else:
    # vacancy not exst, doing insert
    new_insert(job_dict)

mysql_conn.close()
