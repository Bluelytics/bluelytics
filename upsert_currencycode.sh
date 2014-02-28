#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

. $DIR/bin/activate
python $DIR/bluelytics/manage.py upsert_currencycode $1 $2
