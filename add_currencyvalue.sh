#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

. $DIR/bin/activate
python $DIR/bluelytics/manage.py add_currencyvalue $1 $2
