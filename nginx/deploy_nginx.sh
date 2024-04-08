#! /bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: $0 <namespace>"
    exit 1
fi

helm upgrade --install ingress-nginx ingress-nginx --repo https://kubernetes.github.io/ingress-nginx --namespace $1 --values ./values.yaml

if [ $? -ne 0 ]; then
    exit 1
fi
