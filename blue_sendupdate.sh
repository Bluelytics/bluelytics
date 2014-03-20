#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

. $DIR/bin/activate
python $DIR/bluelytics/manage.py blue_sendupdate $1 
