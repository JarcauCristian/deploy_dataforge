#! /bin/bash

if [ $# -ne 4 ]; then
    echo "Usage: $0 <namespace> <minio_endpoint> <minio_access_key> <minio_secret_key>"
    echo "<minio_endpoint>: http(s)://example.com or http(s)://ip_address:port"
    exit 1
fi

namespace="$1"
minio_endpoint="$2"
minio_access_key="$3"
minio_secret_key="$4"
local_address=$(hostname -I | awk '{print $1}')

if [ -z ${KUBE_CONFIG_DEFAULT_LOCATION+x} ]; then
    echo "Please specify the KUBE_CONFIG_DEFAULT_LOCATION environment variable that points to the k3s cluster configuration!"
    exit 1
fi


python3 $PWD/mlflow/run_mlflow.py -n $namespace -a $minio_access_key -e $minio_endpoint -s $minio_secret_key -l $local_address

if [ $? -ne 0 ]; then
    echo "Mlflow deployment failed creating!"
    exit 1
fi
