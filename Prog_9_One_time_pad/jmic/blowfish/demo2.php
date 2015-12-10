<html>
<head>
<title>blowfish demo 2</title>
<meta name="author" content="Jakob Michalka">
<style type="text/css">
<!--
body {
 font-family: Verdana;
}
-->
</style>
</head>
<body text="#000000" bgcolor="#FFFFFF" link="#0000FF" alink="#0000FF" vlink="#0000FF">
<div align="center">
<br>
<h1>blowfish demo 2</h1>
<br>
<?php
include("blowfish.php");
$text = "5,1,2,4,7,1,9,3,8,4,5,1,3,6,1,8,2,3,3,5,9,1,2,2,";
echo "</br>Sudoku solution:";
echo $text;
$key = "blowfish";
keys($key); //Schlüssel Definieren
echo "</br>key:";
echo $key;
$text = blowfish_crypt($text); //Verschlüsseln
echo "</br>Verschlüsseln Text:";
echo $text;
$text = blowfish_decrypt($text); //Entschlüsseln
echo "</br>Unverschlüsselter Text:";
echo $text;
?>
