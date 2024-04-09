#! /bin/bash

if [ $# -ne 2 ]; then
    echo "Usage: $0 <namespace> <os_type>"
    exit 1
fi

namespace="$1"
os_type="$2"
address=$(hostname -I | awk '{print $1}')

if [[ $os_type != "amd" ]] && [[ $os_type != "arm" ]]; then
    echo "Invalid os_type: $os_type. Possible values (arm, amd)"
    exit 1
fi

if [ -z ${KUBE_CONFIG_DEFAULT_LOCATION+x} ]; then
    echo "Please specify the KUBE_CONFIG_DEFAULT_LOCATION environment variable that points to the k3s cluster configuration!"
    exit 1
fi

python3 run_dataset_cronjob.py -n $namespace -a $address -o $os_type

if [ $? -ne 0 ]; then
    echo "Dataset cronjob failed creating!"
    exit 1
fi

