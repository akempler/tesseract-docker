<?php
# Example of sending an image or pdf file.
# run locally with:
# php -S localhost:8080
# Then access at http://localhost:8080/sample-ocr.php

use GuzzleHttp\Client;

require __DIR__ . '/vendor/autoload.php';

// Use the ocr endpoint.
$url = 'http://localhost:5000/api/ocr';

// http://docs.guzzlephp.org/en/stable/
$client = new \GuzzleHttp\Client();

$filename = 'AffidavitArrestWarrant032321.pdf';

$options = [
  'multipart' => [
    [
      'name' => 'file',
      'contents' => fopen('./pdf/' . $filename, 'r'),
      'filename' => $filename,
    ]
  ],
];
$response = $client->post($url, $options);

echo $response->getStatusCode();
echo $response->getHeaderLine('content-type'); 

echo"<pre>";
echo $response->getBody(); 
echo"</pre>";