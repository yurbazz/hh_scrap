<?php
include('db.php');
echo "<a href=\"..\index.php\">На главную страницу</a><br />";

foreach ($_GET as $job_id => $status) {
  $sql = "UPDATE `jobs_info` SET status = $status WHERE `job_id` = $job_id";
  if (mysqli_query($connection, $sql)) {
    echo "<p>Job ".$job_id." status updated</p><br />";
  }
}

mysqli_close($connection);

?>
