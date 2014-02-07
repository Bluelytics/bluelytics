
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

. bin/activate
echo "python bluelytics/manage.py add_blue $1 $2"
python bluelytics/manage.py add_blue $1 $2
