<?php

$connection = mysqli_connect('127.0.0.1', 'jobsdb', 'password', 'JobsDB');
mysqli_set_charset($connection, "utf8");

if ($connection == false) {
	echo'<br> не удалось подключиться к базе данных!<br>';
	echo mysqli_connect_error();
	exit();
}
