<html>
  <header>
    <meta charset="utf-8" />
    <link rel="stylesheet" href="../css/style.css" />
  </header>

<body>
<?php
include('db.php');
echo "<a href=\"..\index.php\">На главную страницу</a>";

$job_status = $_GET['job-status'];

if ($job_status == 'job-new') {
	$sql_filter = "AND j.`status` IS NULL\n";
	$form_header = "<form method=\"GET\" action=\"job_vacancy_set_status.php\">";
	$form_footer = "<button type=\"submit\">Обработать</button>"."</form>";
}
elseif ($job_status == 'job-good') {
	$sql_filter = "AND j.`status` = 1\n";
	$form_header = "";
	$form_footer = "";
}

$sql = "SELECT j.job_id, t.title, c.company, j.p_date AS p_date, j.u_date AS u_date,
j.salary, j.url, j.responsibility, j.requirement, j.updates, j.is_full
FROM `jobs_info` j
JOIN `titles` t
ON j.`title_id` = t.`id`
JOIN `companys` c
ON j.`company_id` = c.`id`
WHERE t.`type` = 1\n" . $sql_filter . "order by j.`id`";

$result = mysqli_query($connection, $sql);
$i = 0;

if ($result->num_rows <> 0) {
	echo $form_header;
  while ($row = mysqli_fetch_assoc($result)) {
		$i += 1;
		echo "<h3>".$i.". ".$row["title"]."</h3>".
		"<ul>".
		"<li>company: ".$row["company"]."</li>".
		"<li>p_date: ".$row["p_date"]."</li>".
		"<li>u_date: ".$row["u_date"]."</li>".
		"<li>salary: ".$row["salary"]."</li>".
		"<li><a href=\"".$row["url"]."\" target=\"_blank\">".$row["url"]."</a></li>".
		"<li>responsibility: ".$row["responsibility"]."</li>".
		"<li>requirement: ".$row["requirement"]."</li>".
		"<li>updates: ".$row["updates"]."</li>".
		"</ul>\n";
		// Если найдены новые вакансии, необходимо выбрать их статус
		if ($job_status == 'job-new') {
			echo "<input type=\"radio\" name=\"".$row["job_id"]."\" value=\"1\" id=\"tracked".$row["job_id"]."\" checked>".
			"<label for=\"tracked".$row["job_id"]."\">Отслеживать</label><br />".
			"<input type=\"radio\" name=\"".$row["job_id"]."\" value=\"2\" id=\"not-tracked".$row["job_id"]."\">".
			"<label for=\"not-tracked".$row["job_id"]."\">Не отслеживать</label><br />\n";
		}
		// Если отмеченная вакансия, показать ссылку на подробное описание
		if ($job_status == 'job-good') {
			if ($row["is_full"] == 1) {
				echo "<form target=\"_blank\" method=\"GET\" action=\"job_vacancy_desc.php\">".
				"<input type=\"hidden\" name=\"job_id\" value=\"".$row["job_id"]."\"/>".
				"<input type=\"hidden\" name=\"title\" value=\"".$row["title"]."\"/>".
				"<input type=\"hidden\" name=\"company\" value=\"".$row["company"]."\"/>".
				"<button type=\"submit\">Подробно</button>".
				"</form>";
			}
		}
  }
	echo $form_footer.
	"</form>";
  mysqli_free_result($result);
}
else {
	echo "<p>Вакансий не найдено.</p>";
}

mysqli_close($connection);

?>

</body>
</html>
