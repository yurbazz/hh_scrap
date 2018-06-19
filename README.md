# Simple hh.ru scraper
Simple project for learning Python through scraping hh.ru.
## Requirements:
### Prerequisites:
* Python 3.5
* Python Modules: lxml, bs4, pymysql
### Files security:
| File        | Group    | Permissions|
|-------------|----------|------------|
| dbconn.py   | www-data | 0750       |
| hh_scrap.py | www-data | 0750       |
| log/        | www-data | 2770       |
| web/db.php  | www-data | 0640       |
