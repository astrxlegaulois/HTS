<html>
<head>
<title>blowfish demo 1</title>
<meta name="author" content="Jakob Michalka">
<style type="text/css">
<!--
body, table {
 font-family: Verdana;
}
-->
</style>
</head>
<body text="#000000" bgcolor="#FFFFFF" link="#0000FF" alink="#0000FF" vlink="#0000FF">
<?php
$key = $_POST['key'];

include("blowfish.php");
$text = trim($_POST['text']);
if(isset($_POST['key'])) keys($_POST['key']); //Schlüssel Definieren

if(isset($_POST["crypt"]))
    {
    $text = blowfish_crypt($text); //Verschlüsseln
    $s = "Verschl&uuml;sselt";
    }

elseif(isset($_POST["decrypt"]))
    {
    $text = blowfish_decrypt($text); //Entschlüsseln
    $s = "Entschl&uuml;sselt";
    }
?>
<br>
<h1 align="center">blowfish demo 1</h1>
<br>
<form action="" method="post" target="">
<table width="80%" border="0" align="center">
<tr>
 <td>Key:</td>
 <td><input type="Text" name="key" value="<?php echo $key; ?>" size="" maxlength="12"></td>
</tr>
<tr>
 <td>Text <? print $s ?>:</td>
 <td><textarea name="text" cols="50" rows="6"><? print $text; ?></textarea></td>
</tr>
<tr>
 <td><input type="Submit" name="crypt" value="Verschlüsseln"></td>
 <td><input type="Submit" name="decrypt" value="Entschlüsseln"></td>
</tr>
</table>
<div align="center"><a href="demo2.php">zu demo 2</a></div>
</form>
</body>
</html>