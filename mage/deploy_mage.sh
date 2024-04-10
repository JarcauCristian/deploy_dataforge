#! /bin/bash

if [ $# -ne 3 ]; then
    echo "Usage: $0 <namespace>"
    exit 1
fi

check_k3s=$(systemctl is-active k3s)

if [[ $check_k3s != "active" ]]; then
    echo "K3s is not installed cannot continue!"
    exit 1
fi

helm repo add mageai https://mage-ai.github.io/helm-charts

helm install mageai mageai/mageai --values ./values.yaml -n "$1"

if [ $? -ne 0 ]; then
    echo "Could not create the deployment!"
else
    echo "Deployment created successfully!"
fi
