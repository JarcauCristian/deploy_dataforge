#! /bin/bash

if [ $# -ne 2 ]; then
    echo "Usage: $0 <namespace> <hostname_for_ui_interface_or_none>"
    exit 1
fi

if [ $]

python run_keycloak.py

if [ $? -ne 0 ]; then
    echo "Could not create the deployment for keycloak."
fi

sleep 30
