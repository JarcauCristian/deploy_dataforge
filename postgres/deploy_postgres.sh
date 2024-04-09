#! /bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: $0 <namespace>"
    exit 1
fi

namespace="$1"
current_user=$(whoami)
address=$(hostname -I | awk '{print $1}')

mkdir /home/$current_user/postgres_data

if [ -z ${KUBE_CONFIG_DEFAULT_LOCATION+x} ]; then
    echo "Please specify the KUBE_CONFIG_DEFAULT_LOCATION environment variable that points to the k3s cluster configuration!"
    exit 1
fi

python3 run_postgres.py -n $namespace -u $current_user -a $address

if [ $? -ne 0 ]; then
    echo "Postgres failed creating!"
    exit 1
fi

sleep 30

python3 create_tables.py -a $address

if [ $? -ne 0 ]; then
    echo "Tables failed creating!"
    exit 1
fi
