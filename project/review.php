<?php session_start();
ob_start();
header("Content-Type:text/event-stream");
header("Cache-Control:no-cache");
	//set_time_limit(0);
	include 'curl.php';
	$number=$_SESSION["number"];
	$make_call = callAPI('GET', 'http://127.0.0.1:5000/api/quiz/questions/review?number='.$number."&username=".$_SESSION["username"],false);
	$response = json_decode($make_call, true);
	//print_r($response);

	$num=0;
	$len=sizeof($response["questions"]);
	foreach($response["questions"] as $question)
	{
		$str="";
		foreach($response["answers"][$num] as $answer)
		{
			$str.=$answer.";";
		}
		echo "event:review\n";
		echo "retry:1000\n";
		echo "data:$question[0];$question[1];$str\n\n";
		$num++;
		
		ob_flush();
		flush();
		//sleep(5);
		 sleep(intval($response["reviewTime"]));
	}

	echo "event:review\n";
		echo "retry:1000\n";
		echo "data: .....\n\n";
	die();


?>