<?php

$connection = mysqli_connect('127.0.0.1', 'jobsdb', 'password', 'JobsDB');
mysqli_set_charset($connection, "utf8");

if ($connection == false) {
	echo'<br> не удалось подключиться к базе данных!<br>';
	echo mysqli_connect_error();
	exit();
}

$job_status = $_GET['job-status'];

if ($job_status == 'job-new') {
	$sql_filter = "AND j.`status` IS NULL\n";
}
elseif ($job_status == 'job-good') {
	$sql_filter = "AND j.`status` = 1\n";
}

  $sql = "SELECT t.title, c.company, j.p_date AS p_date, j.u_date AS u_date,
	j.salary, j.url, j.responsibility, j.requirement, j.updates
  FROM `jobs_info` j
  JOIN `titles` t
  ON j.`title_id` = t.`id`
  JOIN `companys` c
  ON j.`company_id` = c.`id`
  WHERE t.`type` = 1\n" . $sql_filter . "order by j.`id`";

	if ($result = mysqli_query($connection, $sql)) {
    while ($row = mysqli_fetch_assoc($result)) {
			// print_r($row);
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
			"</ul>";
      // printf ("%s (%s)\n", $row["title"], $row["company"]);
    }
    mysqli_free_result($result);
	}


mysqli_close($connection);

?>
