<?php
include('db.php');

echo "<a href=\"..\index.php\">На главную страницу</a>";

$job_status = $_GET['job-status'];

if ($job_status == 'job-new') {
	$sql_filter = "AND j.`status` IS NULL\n";
	$set_tracked = "
	<input type=\"radio\" name=\"".$row["job_id"]."\" value=\"1\" id=\"tracked".$row["job_id"]."\" checked>".
	"<label for=\"tracked".$row["job_id"]."\">Отслеживать</span><br />".
	"<input type=\"radio\" name=\"".$row["job_id"]."\" value=\"2\" id=\"not-tracked".$row["job_id"]."\">".
	"<label for=\"not-tracked".$row["job_id"]."\">Не отслеживать</span><br />\n";
}
elseif ($job_status == 'job-good') {
	$sql_filter = "AND j.`status` = 1\n";
	$set_tracked = "";
}

  $sql = "SELECT j.job_id, t.title, c.company, j.p_date AS p_date, j.u_date AS u_date,
	j.salary, j.url, j.responsibility, j.requirement, j.updates
  FROM `jobs_info` j
  JOIN `titles` t
  ON j.`title_id` = t.`id`
  JOIN `companys` c
  ON j.`company_id` = c.`id`
  WHERE t.`type` = 1\n" . $sql_filter . "order by j.`id`";

	if ($result = mysqli_query($connection, $sql)) {
		echo "<form method=\"GET\" action=\"#\">";
    while ($row = mysqli_fetch_assoc($result)) {
			echo "<h3>".$row["title"]."</h3>".
			"<ul>".
			"<li>company: ".$row["company"]."</li>".
			"<li>p_date: ".$row["p_date"]."</li>".
			"<li>u_date: ".$row["u_date"]."</li>".
			"<li>salary: ".$row["salary"]."</li>".
			"<li><a href=\"".$row["url"]."\">".$row["url"]."</a></li>".
			"<li>responsibility: ".$row["responsibility"]."</li>".
			"<li>requirement: ".$row["requirement"]."</li>".
			"<li>updates: ".$row["updates"]."</li>".
			"</ul>\n".$set_tracked;
    }
		echo "<button type=\"submit\">Обработать</button>".
		"</form>";
    mysqli_free_result($result);
	}


mysqli_close($connection);

?>
