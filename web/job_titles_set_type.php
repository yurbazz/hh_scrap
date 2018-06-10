<?php
include('db.php');
echo "<a href=\"../index.php\">На главную страницу</a><br />";

foreach ($_GET as $id => $type) {
  $sql = "UPDATE `titles` SET type = $type WHERE `id` = $id";
  if (mysqli_query($connection, $sql)) {
    echo "<p>Title ".$id.", type ".$type." set</p><br />";
  }
}

mysqli_close($connection);

?>
