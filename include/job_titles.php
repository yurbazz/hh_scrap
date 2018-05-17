<html>
  <header>
    <meta charset="utf-8" />
    <link rel="stylesheet" href="../css/style.css" />
  </header>

<body>
<?php
include('db.php');
echo "<a href=\"..\index.php\">На главную страницу</a>";

$form_footer = "<button type=\"submit\">Обработать</button>";
$sql = "SELECT id, title FROM `titles` WHERE type IS NULL";

$result = mysqli_query($connection, $sql);

if ($result->num_rows <> 0) {
	echo "<form method=\"GET\" action=\"job_titles_set_type.php\">\n";
  while ($row = mysqli_fetch_assoc($result)) {
		echo "<div class=\"title-block\">".
    "<span class=\"title\">".$row["title"]."</span><br />\n";
		echo "<input type=\"radio\" name=\"".$row["id"]."\" value=\"1\" id=\"tracked".$row["id"]."\">".
		"<label for=\"tracked".$row["id"]."\">Отслеживать</label><br />".
		"<input type=\"radio\" name=\"".$row["id"]."\" value=\"2\" id=\"not-tracked".$row["id"]."\" checked>".
		"<label for=\"not-tracked".$row["id"]."\">Не отслеживать</label><br />\n".
    "</div>";
		}
  echo $form_footer.
  "</form>";
  mysqli_free_result($result);
  }
else {
	echo "<p>Должностей не найдено.</p>";
}

mysqli_close($connection);

?>

</body>
</html>
