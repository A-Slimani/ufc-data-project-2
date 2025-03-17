#!/bin/bash

LOCAL_SOURCE="."
REMOTE_USER="aboud"
REMOTE_HOST="10.0.0.216"
REMOTE_DEST="/home/aboud/programming/ufc-data/"

rsync -av \
  --filter=':- .gitignore' \
  --exclude={'.vscode','.DS_Store','.git/'} \
  $LOCAL_SOURCE $REMOTE_USER@$REMOTE_HOST:$REMOTE_DEST

docker-compose --context remote up --build -d