#!/bin/bash

set -e

while ! /bin/nc -z zenoss4-mariadb 3306;
  do
    echo "Waiting for zenoss4-mariadb to initialize...";
    sleep 1;
  done;

echo "zenoss4-mariadb started! Launching the zenoss daemons..."
#service zenoss start & tail -f /usr/local/zenoss/log/Z2.log
service zenoss start & tail -f /dev/null
