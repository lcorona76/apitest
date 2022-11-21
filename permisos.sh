#!/bin/bash

# si número de parámetros menor o igual que 0 
#if [ $1 -le 0 ]
#then
#  echo "Hay que introducir al menos un parámetro."
#  exit 1
#fi

PERMISO=$(/usr/bin/ls -l $1 | cut -d " " -f 1)
USER=$(/usr/bin/ls -l $1 | cut -d " " -f 3)
GROUP=$(/usr/bin/ls -l $1 | cut -d " " -f 4)
HASH=$(/usr/bin/sha256sum $1)
ATIME=$(/usr/bin/stat $1 | grep "Access: [0-9]" | cut -d " " -f 2-3)
MTIME=$(/usr/bin/stat $1 | grep Modify: | cut -d " " -f 2-3)
echo \{\"permissions\": \{\"permission\": \"$PERMISO\",\"user\": \"$USER\",\"group\": \"$GROUP\"\},\"SHA256\": \"$HASH\",\"timestamps\"\: \{\"atime\": \"$ATIME\",\"mtime\": \"$MTIME\"\}\}
