<html>
  <header>
    <meta charset="utf-8" />
    <link rel="stylesheet" href="../css/style.css" />
  </header>

<body>
<?php
include('db.php');

$job_id = $_GET['job_id'];
$title = $_GET['title'];
$company = $_GET['company'];

$sql = "SELECT description FROM `jobs_desc` WHERE job_id = ".$job_id;
$result = mysqli_query($connection, $sql);

while ($row = mysqli_fetch_assoc($result)) {
  echo "<div class=\"desc-block\">\n".
  "<h3>".$title."</h3>".
  "<p>Работодатель: <i>".$company."</i></p>".
  $row['description'].
  "</div>";
}
mysqli_free_result($result);
?>

</body>
</html>
