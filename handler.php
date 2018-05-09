<?php

$connection = mysqli_connect('127.0.0.1','jobsdb','password','JobsDB');

if($connection == false){
	echo'<br> не удалось подключиться к базе данных!<br>';
	echo mysqli_connect_error();
	exit();
}

$job_status = $_GET['job-status'];

if ($job_status == 'job-new') {
  $sql = "SELECT t.title, c.company, j.p_date, j.salary, j.url, j.responsibility, j.requirement, j.updates, j.status
  FROM `jobs_info` j
  JOIN `titles` t
  ON j.`title_id` = t.`id`
  JOIN `companys` c
  ON j.`company_id` = c.`id`
  WHERE t.`type` = 1
  AND j.`status` IS NULL 	 # для новых вакансий
  order by j.`id`";
  $result = mysqli_query($connection,$sql);
  $row = mysqli_fetch_assoc($result);
  print_r($row);
}

?>
