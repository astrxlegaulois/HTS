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
include("sudoku_seb.php");
$text = "6,5,,7,8,,,2,,3,,,,,,7,,9,9,,,1,2,,4,5,6,2,1,9,3,4,5,6,7,8,5,,,6,7,8,9,1,,8,7,6,9,1,2,3,4,5,7,6,,8,9,1,,3,4,4,3,2,,6,7,8,,1,1,9,8,,,,5,6,";
echo "</br>Sudoku reading:";
$sudoku=initSudoku($text);
echo $sudoku;
echo "</br>Sudoku solving:";
$sudoku=resolutionSimple($sudoku);
echo $sudoku;
echo "</br>Sudoku parsing:";
$result=sudokuToString($sudoku);
echo $result;
echo "</br>Sha1:";
$result=sha1($result);
echo $result;
echo "</br>Blowfish key generation:";
keys($result); //Schlüssel Definieren
echo "</br>key:";
echo $key;
echo "</br>Blowfish key generation:";
//$text = blowfish_crypt($text); //Verschlüsseln
$encrypted="Vm6c7wAK15IeEvUBshqV2g==";
echo "</br>Verschlüsseln Text:";
echo $encrypted;
$decrypted = blowfish_decrypt($encrypted); //Entschlüsseln
echo "</br>Unverschlüsselter Text:";
echo $decrypted;
?>
