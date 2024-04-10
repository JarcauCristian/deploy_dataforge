#! /bin/bash

if [ $# -ne 2 ]; then
    echo "Usage: $0 <namespace> <hostname_for_ui_interface_or_none>"
    exit 1
fi

address=$(hostname -I | awk '{print $1}')

if [ -z ${KUBE_CONFIG_DEFAULT_LOCATION+x} ]; then
    echo "Please specify the KUBE_CONFIG_DEFAULT_LOCATION environment variable that points to the k3s cluster configuration!"
    exit 1
fi


python3 $PWD/keycloak/run_keycloak.py -a $address -n $1

if [ $? -ne 0 ]; then
    echo "Could not create the deployment for keycloak."
fi

sleep 30

if [ "$2" = "" ]; then
    python3 $PWD/keycloack/create.py
else
    python3 $PWD/keycloack/create.py -a $host
fi

if [ $? -ne 0 ]; then
    echo "Could not create the realms and clients inside keycloak."
fi
