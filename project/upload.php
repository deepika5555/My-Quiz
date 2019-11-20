<?php
include("curl.php");
	$target_dir = "uploads/";
	$target_file = $target_dir . basename($_FILES["imgB64"]["name"]);
	(move_uploaded_file($_FILES["imgB64"]["tmp_name"], $target_file));
    $path="uploads/".$_FILES["imgB64"]["name"];

	$d=file_get_contents($path);
    $img=base64_encode($d);

    $num=$_POST['number'];
	$imageFileType = strtolower(pathinfo($target_file,PATHINFO_EXTENSION));
    if($imageFileType != "jpg") 
    {
    	$data_array =  array("base64_str"=>$img,"file_type"=>$imageFileType,'number'=>$num);
    }
    else if($imageFileType != "png") 
    {
    	$data_array =  array("base64_str"=>$img,"file_type"=>$imageFileType,'number'=>$num);
    }
    else if($imageFileType != "pdf") 
    {
    
    	$data_array =  array("base64_str"=>$img,"file_type"=>$imageFileType,'number'=>$num);
    }


$make_call = callAPI('POST', 'http://127.0.0.1:5000/api/quiz/file', json_encode($data_array));
$response = json_decode($make_call, true);
echo "<script>window.location.href='home.html';</script>";
?>