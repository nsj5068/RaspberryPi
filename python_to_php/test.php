<?php
    header("charset=UTF-8");

    $_id       = $_POST['_id'];
    $temp_1    = $_POST['temp_1'];
    $humid_1   = $_POST['humid_1'];

    include "./dbconn.php";

    if(!$connect) {
        echo "Error";
        exit;
    }

    $sql = "INSERT INTO nsj_test(_id, temp_1, humid_1) VALUES('$_id', '$temp_1', '$humid_1');";
    

    $result = mysqli_query($connect, $sql);
    mysqli_close($conncet);

    echo "Save OK";

?>
