    <?php

	echo "Hello <br/>";
      //------------------------------------------------------------------------------------
      function evalCrossTotal($strMD5)
      {
          $intTotal = 0;
          $arrMD5Chars = str_split($strMD5, 1);
          foreach ($arrMD5Chars as $value)
          {
              $intTotal += '0x0'.$value;
          }
          return $intTotal;
      }//-----------------------------------------------------------------------------------



      //------------------------------------------------------------------------------------
      function encryptString($strString, $strPassword)
      {
          // $strString is the content of the entire file with serials
          echo "strString: ".$strString."<br/>";
          echo "strPassword: ".$strPassword."<br/>";
          //$strPasswordMD5 = md5($strPassword);
          $strPasswordMD5 = '00000000000000000000000000000000';
          echo "strPasswordMD5: ".$strPasswordMD5."<br/>";
          $intMD5Total = evalCrossTotal($strPasswordMD5);
          echo "intMD5Total: ".$intMD5Total."<br/>";
          $arrEncryptedValues = array();
          $intStrlen = strlen($strString);
          echo "intStrlen: ".$intStrlen."<br/>";
          for ($i=0; $i<$intStrlen; $i++)
          {
			  echo "i: ".$i."<br/>";
              $arrEncryptedValues[] =  ord(substr($strString, $i, 1)) +  ('0x0' . substr($strPasswordMD5, $i%32, 1)) -  $intMD5Total;
              echo "ord: ".ord(substr($strString, $i, 1))."<br/>";
              echo "substr(strPasswordMD5: ".('0x0' . substr($strPasswordMD5, $i%32, 1))."<br/>";
              echo "intMD5Total: ".$intMD5Total."<br/>";
              $temp=ord(substr($strString, $i, 1)) +  ('0x0' . substr($strPasswordMD5, $i%32, 1)) -  $intMD5Total;
              echo "temp: ".$temp."<br/>";
              $intMD5Total = evalCrossTotal(substr(md5(substr($strString,0,$i+1)), 0, 16).substr(md5($intMD5Total), 0, 16));
              echo "newintMD5Total: ".$intMD5Total."<br/><br/>";
          }
          return implode(' ' , $arrEncryptedValues);
      }//-----------------------------------------------------------------------------------

	echo "working :".encryptString("\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0","");
	


echo "<br/>Bye <br/>";
    ?>
