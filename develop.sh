#!/bin/bash
set -e

# Triggered when the user interrupts the script to stop it.
trap quitjobs INT
quitjobs() {
    echo ""
    pkill -P $$
    echo "Killed all running jobs".
    scriptCancelled="true"
    trap - INT
    exit
}

# Wait for user input so the jobs can be quit afterwards.
scriptCancelled="false"
waitforcancel() {
    while :
    do
        if [ "$scriptCancelled" == "true" ]; then
            return
        fi
        sleep 1
    done
}

# The actual commands we want to execute.
DIR=$(pwd)
cd $DIR/backend && FLASK_APP=main.py FLASK_ENV=development python -m flask run --host 0.0.0.0 &
cd $DIR/frontend && bash -c 'COLOR=1 BROWSER=none yarn run start | cat' &

# Trap the input and wait for the script to be cancelled.
waitforcancel
return 0