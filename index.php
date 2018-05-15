<html lang="ru">
  <head>
    <title>Просмотр вакансий HH</title>
    <meta charset="utf-8" />
    <link rel="stylesheet" href="css/style.css" />
  </head>
  <body>
    <form method="GET" action="include/handler.php">
      <h2>Статус вакансий:</h2>
      <input type="radio" name="job-status" id="job-new" value="job-new" checked />
      <label for="job-new">новые</label>
      <input type="radio" name="job-status" id="job-good" value="job-good" />
      <label for="job-good">уже отмеченные</label>
      <button type="submit">Найти</button>
    </form>
  </body>
</html>
