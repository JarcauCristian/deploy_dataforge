#! /bin/bash

if [ $# -ne 2 ]; then
    echo "Usage: $0 <namespace> <os_type>"
    exit 1
fi

namespace="$1"
os_type="$2"

if [[ $os_type != "amd" ]] && [[ $os_type != "arm" ]]; then
    echo "Invalid os_type: $os_type. Possible values (arm, amd)"
    exit 1
fi

if [ -z ${KUBE_CONFIG_DEFAULT_LOCATION+x} ]; then
    echo "Please specify the KUBE_CONFIG_DEFAULT_LOCATION environment variable that points to the k3s cluster configuration!"
    exit 1
fi


python3 $PWD/interface/run_ui.py -n $namespace -o $os_type

if [ $? -ne 0 ]; then
    echo "User interface failed creating!"
    exit 1
fi
