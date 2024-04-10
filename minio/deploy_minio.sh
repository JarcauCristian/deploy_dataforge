#! /bin/bash

if [ $# -ne 3 ]; then
    echo "Usage: $0 <username> <password> <namespace>"
    exit 1
fi

check_k3s=$(systemctl is-active k3s)

if [[ $check_k3s != "active" ]]; then
    echo "K3s is not installed cannot continue!"
    exit 1
fi

helm dependency update

if [ $? -ne 0 ]; then
    echo "Could not update minio dependencies!"
    exit 1
fi

python3 $PWD/minio/update_values.py -u $1 -p $2

helm install minio-realease minio --values ./values.yaml -n $3

if [ $? -ne 0 ]; then
    echo "Could not create the deployment!"
else
    echo "Deployment created successfully!"
fi
