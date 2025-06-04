<?php
$file = $_GET['file'];
if (include($file)) {
    echo "File included successfully";
}else {
    http_response_code(403);
    echo "File inclusion failed";
}
?>
