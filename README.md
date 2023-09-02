# A Docker environment for working with Tesseract (Pytesseract).

## Overview
Provides dockerized access to:
* Tesseract (via pytesseract)

NOTE: this is built for local development, and not really suited to production environments yet.

## Installation and Setup
Clone this repo.

```docker-compose build```
```docker-compose up```

## Usage / API
These endpoints are available at:
http://localhost:5000

### OCR / Tesseract
Uses tesseract to retrieve the text from an image. 
This could be a standard image format such as jpg or png, 
or it could be a PDF.

#### `POST` `/api/ocr`

```
{
  "file": <A source pdf file>
}
```

Name | Type | Description
------------ | ------------- | -------------
file | file resource | The file to process for text.
psm | page segmentation mode | Which tesseract psm mode to use. Defaults to 3.
oem | engine mode | Which tesseract engine mode to use. Defaults to 3.


Example request using [GuzzleHttp](http://docs.guzzlephp.org/en/stable/):

```
$body = fopen('/path/to/file', 'r');
$r = $client->request('POST', 'http://localhost:5000/api/ocr', ['file' => $body]);
```

Example response:

```
{
  "lines": [
    "The (quick) [brown] {fox} jumps!",
    "Over the $43,456.78 <lazy> #90 dog",
    "& duck/goose, as 12.5% of E-mail",
    "from aspammer@website.com is spam.",
    "Der ,.schnelle” braune Fuchs springt",
    "iiber den faulen Hund. Le renard brun",
    "«rapide» saute par-dessus le chien",
    "paresseux. La volpe marrone rapida",
    "salta sopra il cane pigro. El zorro",
    "marron rapido salta sobre el perro",
    "perezoso. A raposa marrom rapida",
    "salta sobre o céo preguicoso."
  ],
  "text": "The (quick) [brown] {fox} jumps!\nOver the $43,456.78 <lazy> #90 dog\n& duck/goose, as 12.5% of E-mail\nfrom aspammer@website.com is spam.\nDer ,.schnelle” braune Fuchs springt\niiber den faulen Hund. Le renard brun\n«rapide» saute par-dessus le chien\nparesseux. La volpe marrone rapida\nsalta sopra il cane pigro. El zorro\nmarron rapido salta sobre el perro\nperezoso. A raposa marrom rapida\nsalta sobre o céo preguicoso."
}
```

Detailed example, specifying a different psm:

```
<?php

use GuzzleHttp\Client;
require __DIR__ . '/vendor/autoload.php';

$url = 'http://localhost:5000/api/ocr';
$client = new \GuzzleHttp\Client();

$options = [
    'multipart' => [
        [
            'contents' => fopen('./pdf/H3485-2019-01-09-introduced.pdf', 'r'),
            'filename' => 'H3485-2019-01-09-introduced.pdf',
        ],
        [
            'name' => 'psm',
            'contents' => json_encode('11')
        ]
    ],
];
$response = $client->post($url, $options);

echo $response->getStatusCode(); // 200
echo"<pre>";
echo $response->getBody(); 
echo"</pre>";
```

Response:
```
{
  "lines": [
    "SOUTH CAROLINA REVENUE AND FISCAL AFFAIRS OFFICE",
    "STATEMENT OF ESTIMATED FISCAL IMPACT",
    "(803)734-0640 » RFA.SC.GOV/IMPACTS",
    "Bill Number:",
    "H. 3020",
    "Introduced on January 8, 2019",
    "Author:",
    "MeCravy",
    "Subject:",
    "SC Fetal Heartbeat Protection from Abortion Act",
    "Requestor:",
    "House Judiciary",
    "RFA Analyst(s):",
    "Griffith and Gardner",
    "Impact Date:",
    "April 4, 2019",
    "Fiscal Impact Summary",
    "This bill will have no expenditure impact on the General Fund, Federal Funds, or Other Funds",
  ],
    "text": "SOUTH CAROLINA REVENUE AND FISCAL AFFAIRS OFFICE STATEMENT OF ESTIMATED FISCAL IMPACT (803)734-0640 » RFA.SC.GOV/IMPACTS Bill Number: H. 3020 Introduced on January 8, 2019 Author: MeCravy Subject: SC Fetal Heartbeat Protection from Abortion Act Requestor: House Judiciary RFA Analyst(s): Griffith and Gardner Impact Date: April 4, 2019 Fiscal Impact Summary This bill will have no expenditure impact on the General Fund, Federal Funds, or Other Funds becat any additional expenses relating to the promulgation..."
}
```
