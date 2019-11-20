<?php

	extract($_GET);
	echo "<script>localStorage.setItem('number','".$number."');";
	echo "window.location.href='quiz.html';</script>";
?>