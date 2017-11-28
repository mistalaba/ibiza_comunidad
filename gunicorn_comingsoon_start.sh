#!/bin/bash
set -e
HOME=/home/mistalaba
VENV=$HOME/.virtualenvs/ibiza_comunidad
LOGFILE=$HOME/logs/gunicorn_ibiza_comunidad_comingsoon.log
LOGDIR=$(dirname $LOGFILE)
NUM_WORKERS=1
ADDRESS=0.0.0.0:8001
cd $HOME/projects/ibiza_comunidad
source $VENV/bin/activate
test -d $LOGDIR || mkdir -p $LOGDIR
exec gunicorn config.wsgi_comingsoon:application -w $NUM_WORKERS --max-requests 500 --timeout 600 --bind=$ADDRESS --log-level=info --log-file=$LOGFILE 2>>$LOGFILE
