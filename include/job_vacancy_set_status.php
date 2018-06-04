<?php
include('db.php');
echo "<a href=\"..\index.php\">На главную страницу</a><br />";

$status = 0;

foreach ($_GET as $key => $value) {
  if (preg_match('/^[1-9]+/',$key)) {
    // Set job status
    $sql = "UPDATE `jobs_info` SET status = $value WHERE `job_id` = $key";
    echo $sql."<br />";
    if (mysqli_query($connection, $sql)) {
      echo "<p>Job ".$key." status updated</p><br />";
    }
    $status = $value;
  }
  elseif (preg_match('/joburl/',$key)) {
    // Scrap description for tracked job
    if ($status == 1) {
      $command = escapeshellcmd('../hh_scrap.py -d '.$key);
      $output = shell_exec($command);
      echo $output."<br />";
    }
  }
}

mysqli_close($connection);

?>
