<?php
include("curl.php");
	extract($_POST);
	$data_array =  array("username"=>$username,"password"=>$pass,'dob'=>$date,'emailId'=>$email,'phone'=>$phone);
	$make_call = callAPI('POST', 'http://127.0.0.1:5000/api/user', json_encode($data_array));
	$response = json_decode($make_call, true);
	echo "<script>alert('user details created');localStorage.setItem('username',".$username."') window.location.href='home.html';</script>"
?>