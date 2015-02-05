#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd $DIR
. $DIR/bin/activate
python $DIR/bluelytics/manage.py update_bcra ../bcra_scrape/out/
python $DIR/bluelytics/manage.py export_bcra bluelytics/data/graphs/bcra.json
