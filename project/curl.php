<?php
ini_set('display_errors',1);
error_reporting(E_ALL);
function callAPI($method, $url, $data){
   $curl = curl_init();

   switch ($method){
      case "POST":
         curl_setopt($curl, CURLOPT_POST, 1);
         if ($data)
            curl_setopt($curl, CURLOPT_POSTFIELDS, $data);
         break;
      case "PUT":
         curl_setopt($curl, CURLOPT_CUSTOMREQUEST, "PUT");
         if ($data)
            curl_setopt($curl, CURLOPT_POSTFIELDS, $data);			 					
         break;
      case "DELETE":
         curl_setopt($curl, CURLOPT_URL, $url);
         curl_setopt($curl, CURLOPT_CUSTOMREQUEST, "DELETE");			 					
         break;
      default:
         if ($data)
            $url = sprintf("%s?%s", $url, http_build_query($data));
   }

   // OPTIONS:
   curl_setopt($curl, CURLOPT_URL, $url);
   curl_setopt($curl, CURLOPT_HTTPHEADER, array(
      'APIKEY: 111111111111111111111',
      'Content-Type: application/json',
   ));
   curl_setopt($curl, CURLOPT_RETURNTRANSFER, 1);
   curl_setopt($curl, CURLOPT_HTTPAUTH, CURLAUTH_BASIC);

   // EXECUTE:
   $result = curl_exec($curl);
   if(!$result){die("Connection Failure");}
   curl_close($curl);
   return $result;
}

/*$get_data = callAPI('GET', 'http://127.0.0.1:5000/api/v1/categories', false);
$response = json_decode($get_data, true);
//$errors = $response['response']['errors'];
$data = $response['message'];
$data_array =  array(
  "username"=>'john',
  'password'=>'111111'
);

$make_call = callAPI('POST', 'http://127.0.0.1:5000/api/v1/users', json_encode($data_array));
$response = json_decode($make_call, true);
//$errors   = $response['response']['errors'];
echo $make_call;
$data     = $response['message'];
$a=callAPI('DELETE', 'http://127.0.0.1:5000/api/v1/users/john', false);
echo $a;

*/
?>    
