<?php session_start();
ob_start();
header("Content-Type:text/event-stream");
header("Cache-Control:no-cache");
	//set_time_limit(0);
	$number=$_SESSION["number"];
	include 'curl.php';
	$make_call = callAPI('GET', 'http://127.0.0.1:5000/api/quiz/questions?number='.$number."&username=".$_SESSION["username"],false);
	$response = json_decode($make_call, true);
	//print_r($response);
	if($response["msg"]=="null")
	{	echo "event:quiz\n";
		echo "data: ..\n\n";
	}
	else
{
	$num=0;

	$len=sizeof($response["questions"]);
	foreach($response["questions"] as $question)
	{
		$str="";
		foreach($response["answers"][$num] as $answer)
		{
			$str.=$answer.";";
		}
		echo "event:quiz\n";
		echo "retry:1000\n";
		echo "data:$question[0];$str\n\n";
		$num++;
		
		ob_flush();
		flush();
		//sleep(5);
		sleep(intval($response["answerTime"]));
	}

	echo "event:quiz\n";
		echo "retry:1000\n";
		echo "data: .....\n\n";
	die();
}

?>