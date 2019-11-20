<?php session_start();
	session_destroy();
	echo "<script>localStorage.removeItem('number');localStorage.removeItem('username');window.location.href='login.html';</script>"
?>