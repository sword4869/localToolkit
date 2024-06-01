#! /bin/bash
if [ -z $1 ];
then 
    echo "python -m http.server 8000"
    python -m http.server 8000;
else
    echo "python -m http.server 8000 --directory $(dirname $(readlink -f "$1"))"
    python -m http.server 8000 --directory $1;
fi
