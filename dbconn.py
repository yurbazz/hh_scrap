import logging
import pymysql.cursors


def set_conn():
    conn = pymysql.connect(host='localhost',
                           user='jobsdb',
                           password='password',
                           db='JobsDB',
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.Cursor)
    return conn


def new_insert(conn, job_dict):
    logging.debug("New job found, doing insert")
    try:
        with conn.cursor() as cur:
            sql = "SELECT title FROM `titles` WHERE `title` = %s"
            if cur.execute(sql, job_dict['title']) == 0:
                logging.debug("Title: [%s] not found, insert to db" % job_dict['title'])
                sql = "INSERT INTO `titles` (`title`) VALUES (%s)"
                cur.execute(sql, (job_dict['title']))
                conn.commit()
                logging.debug("Title: [%s] inserted" % job_dict['title'])
            sql = "SELECT id FROM `titles` WHERE `title` = %s"
            cur.execute(sql, job_dict['title'])
            job_dict['title_id'] = int(cur.fetchone()[0])
        with conn.cursor() as cur:
            sql = "SELECT company FROM `companys` WHERE `company` = %s"
            if cur.execute(sql, job_dict['company']) == 0:
                logging.debug("Company: [%s] not found, insert to db" % job_dict['company'])
                sql = "INSERT INTO `companys` (`company`) VALUES (%s)"
                cur.execute(sql, job_dict['company'])
                conn.commit()
                logging.debug("Company: [%s] inserted" % job_dict['company'])
            sql = "SELECT id FROM `companys` WHERE `company` = %s"
            cur.execute(sql, job_dict['company'])
            job_dict['company_id'] = int(cur.fetchone()[0])
        with conn.cursor() as cur:
            sql = "INSERT INTO `jobs_info` " \
                  "     (`job_id`, `title_id`, `company_id`, `p_date`, `u_date`, `salary`, `url`, `responsibility`, " \
                  "     `requirement`, `promo`, `updates`) " \
                  "VALUES (%(id)s, %(title_id)s, %(company_id)s, %(date)s, %(date)s, %(salary)s, %(url)s, " \
                  "        %(responsibility)s, %(requirement)s, %(promo)s, 0)"
            cur.execute(sql, job_dict)
            conn.commit()
            logging.debug("Job with id [%s], title[%s] inserted to db" % (job_dict['id'],job_dict['title']))
    except pymysql.err.Error as e:
        logging.error(e)


def job_handler(job_dict):
    conn = set_conn()
    try:
        with conn.cursor() as cur:
            # Check if we get all new vacancies and can stop...
            sql = "SELECT 1 FROM `jobs_info` WHERE `job_id` = %s AND `u_date` = %s"
            if cur.execute(sql, (job_dict['id'], job_dict['date'])) == 1:
                logging.debug("It seems we found all new jobs. This job is already in db: id[%s], date[%s], "
                              "title[%s]..." % (job_dict['id'], job_dict['date'], job_dict['title']))
                # ...But not if old vacancy is in promo list
                sql = "SELECT promo FROM `jobs_info` WHERE `job_id` = %s"
                cur.execute(sql, job_dict['id'])
                if cur.fetchone()[0] == 1:
                    logging.debug("...But it's a promo, so continue")
                    return
                else:
                    logging.info("=== SCRAPER STOPED ===")
                    exit()
            else:
                sql = "SELECT type FROM `titles` WHERE `title` = %s"
                # If found 0 rows doing new insert
                if cur.execute(sql, job_dict['title']) == 0:
                    new_insert(conn, job_dict)
                    return 1
                # Skip if vacancy is not interesting
                if cur.fetchone()[0] == 2:
                    logging.debug("Title: [%s] not interesting, exlude" % job_dict['title'])
                    return
        with conn.cursor() as cur:
            # Check if vacancy is exist and confirmed on new date
            sql = "SELECT 1 FROM `jobs_info` WHERE `job_id` = %s AND " \
                  "`title_id` = (SELECT id FROM `titles` WHERE `title` = %s)"
            if cur.execute(sql, (job_dict['id'], job_dict['title'])) == 1:
                logging.debug("The job with id[%s], title[%s], was updated on date[%s]" %
                              (job_dict['id'], job_dict['title'], job_dict['date']))
                # Update date of confirmation
                sql = "UPDATE `jobs_info` SET `u_date` = %s, `updates` = `updates` + 1 WHERE `job_id` = %s"
                cur.execute(sql, (job_dict['date'], job_dict['id']))
                conn.commit()
                logging.debug("Date updated, go to next job")
                return
            else:
                # vacancy not exist, doing insert
                new_insert(conn, job_dict)
    except pymysql.err.Error as e:
        logging.error(e)
    finally:
        conn.close()
