#! /bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: $0 <namespace>"
    exit 1
fi

if [ -z ${KUBE_CONFIG_DEFAULT_LOCATION+x} ]; then
    echo "Please specify the KUBE_CONFIG_DEFAULT_LOCATION environment variable that points to the k3s cluster configuration!"
    exit 1
fi


helm uninstall minio-realease

if [ $? -ne 0 ]; then
    echo "Could not delete nginx ingress controller!"
fi
