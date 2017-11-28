#!/bin/bash
set -e
HOME=/home/mistalaba
VENV=$HOME/.virtualenvs/ibiza_comunidad
LOGFILE=$HOME/logs/celery_ibiza_comunidad.log
LOGDIR=$(dirname $LOGFILE)
NUM_WORKERS=1
ADDRESS=0.0.0.0:8000
cd $HOME/projects/ibiza_comunidad
source $VENV/bin/activate
test -d $LOGDIR || mkdir -p $LOGDIR
celery -A ibiza_comunidad.taskapp worker -l info --concurrency=1 --maxtasksperchild=1000 --logfile=$LOGFILE 2>>$LOGFILE
