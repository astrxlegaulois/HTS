<?php

    echo "begin Sudoku Lib</br>"; 
   
    // Generates a sudoku table according to the coma separated input string
    // Input sample : 6,3,9,7,,,5,,,7,4,1,,2,5,,3,9,8,,2,,,6,7,,1,3,9,6,,7,1,,8,,,,7,,8,2,3,9,,,2,,,,,,,7,9,6,3,1,,,,5,,,7,,,,8,,6,3,,8,5,3,,,1,,4
    function initSudoku($inputString){
        $tempArray=split(",", $inputString);
        for ($k=0;$k<9*9;$k++) $sudoku[$k/9][$k%9]=$tempArray[$k];
        return $sudoku;
    }
    
    // Generates a coma separated string from a Sudoku
    function sudokuToString($sudoku){
        $str;
        for ($i=0;$i<9;$i++){
            for ($j=0;$j<9;$j++){
                $str .= $sudoku[$i][$j] . ",";
            }
        }
        $str = trim($str, ',');//removes the final comma 
        return $str;
    }
    
    // Solves a sudoku, using the allowed numbers per square method
    function resolutionSimple(&$sudoku){
      //int permissions[9][9][9],i,j,k;
      for ($i=0;$i<9;$i++){ //initialisation
        for ($j=0;$j<9;$j++){
          for ($k=0;$k<9;$k++)$permissions[$i][$j][$k]=0;
        }
      }
      $k=1;
      while($k>0){
        $permissions=interdictions($permissions,$sudoku);
        $k=solutionsSimples($permissions,$sudoku);
      }
      return($sudoku);
    }
    
    //Finds the obvious solutions for the available squares
    function solutionsSimples(&$permissions,&$sudoku){
      $trouvees=0;
      for ($i=0;$i<9;$i++){
        for ($j=0;$j<9;$j++){ 
            $l=0;
            for ($k=0;$k<9;$k++) $l+=$permissions[$i][$j][$k];
            if (($l==8)&&($sudoku[$i][$j]==0)) {
              for($k=0;$k<9;$k++){
                if ($permissions[$i][$j][$k]==0){
                  $sudoku[$i][$j]=($k+1);
                  $trouvees++;
                } 
              }
            }
        }
      }
        return($trouvees);
    }

    //Forbids the numbers on the whole sudoku
    function interdictions(&$permissions, $sudoku){
      for ($pi=0;$pi<9;$pi++){
        for ($pj=0;$pj<9;$pj++){
          if($sudoku[$pi][$pj]!=0){
            for($pk=0;$pk<9;$pk++)$permissions[$pi][$pj][$pk]=1;
            $permissions=interdire($permissions,$pi,$pj,$sudoku[$pi][$pj]);
          }
        }
      }
      return $permissions;
    }

    // Forbids on line, on row and 9-square
    function interdire(&$permissions,$x,$y,$nombre){
      for ($i=0;$i<9;$i++){
        $permissions[$x][$i][$nombre-1]=1;  
      }
      for ($i=0;$i<9;$i++){
        $permissions[$i][$y][$nombre-1]=1;  
      }
      $k=$x%3;
      $l=$y%3;
      for ($j=2-$l;$j<(2+3-$l);$j++){
        for ($i=2-$k;$i<(2+3-$k);$i++){
          $permissions[$x+$i-2][$y+$j-2][$nombre-1]=1;
        }
      }
      return $permissions;
    }
    
    echo "end Sudoku Lib</br>";
?>
