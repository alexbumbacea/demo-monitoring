<?php

$message = sprintf(
'working_time#method=%s,lang=%s,langVersion=%s:%d|ms',
    $_SERVER['REQUEST_METHOD'],
    'php',
    PHP_VERSION,
    floatval(mt_rand(50, 90000)) *1000
);
header('demo: ' . $message);

if ($socket = socket_create(AF_INET, SOCK_DGRAM, SOL_UDP)) {
    socket_sendto($socket, $message, strlen($message), 0, "statsd-exporter", "9125");
    socket_close($socket);
}

echo "This is PHP!";