#! /bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: $0 <namespace>"
    exit 1
fi

if [ -z ${KUBE_CONFIG_DEFAULT_LOCATION+x} ]; then
    echo "Please specify the KUBE_CONFIG_DEFAULT_LOCATION environment variable that points to the k3s cluster configuration!"
    exit 1
fi

python3 $PWD/redis/run_redis.py -n "$1"

if [ $? -ne 0 ]; then
    echo "Could not create a redis server."
fi
