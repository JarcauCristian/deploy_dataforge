#! /bin/bash

if [ $# -ne 5 ]; then
    echo "Usage: $0 <namespace> <os_type> <username_neo4j_db> <password_neo4j_db>"
    exit 1
fi

namespace="$1"
os_type="$2"
username="$4"
password="$5"

address=$(hostname -I | awk '{print $1}')

neo4j_service="$(systemctl is-active neo4j)"
if [[ $neo4j_service != "active" ]]; then
    echo "Please have a local clean neo4j database installed!"
    exit 1
fi

python3 create_base_database.py -a $address -u $username -p $password

if [ $? -ne 0 ]; then
    echo "Neo4j API failed creating!"
    exit 1
fi


if [[ $os_type != "amd" ]] && [[ $os_type != "arm" ]]; then
    echo "Invalid os_type: $os_type. Possible values (arm, amd)"
    exit 1
fi

if [ -z ${KUBE_CONFIG_DEFAULT_LOCATION+x} ]; then
    echo "Please specify the KUBE_CONFIG_DEFAULT_LOCATION environment variable that points to the k3s cluster configuration!"
    exit 1
fi

python3 run_neo4j_api.py -n $namespace -a $address -o $os_type -u $username -p $password

if [ $? -ne 0 ]; then
    echo "Neo4j API failed creating!"
    exit 1
fi

