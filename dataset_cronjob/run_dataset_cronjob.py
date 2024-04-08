import os
import yaml
import argparse
from kubernetes import client, config
from kubernetes.client.rest import ApiException

parser = argparse.ArgumentParser()

parser.add_argument("-a", "--addr", type=str, help="Address for postgres db!", required=True)
parser.add_argument("-n", "--namespace", type=str, help="Namespace to run the deployment on!", required=True)

args = parser.parse_args()

def main():

    if not os.path.exists("/etc/rancher/k3s/k3s.yaml"):
        exit(1)

    config.load_config()
    apps_v1_api = client.AppsV1Api()
    core_v1_api = client.CoreV1Api()

    if os.path.exists("./cronjob.yaml"):
        with open("./cronjob.yaml", "r") as f:
            cronjob = yaml.safe_load(f)
        cronjob["metadata"]["namespace"] = args.namespace
        cronjob["spec"]["jobTemplate"]["spec"]["template"]["spec"]["env"][3]["value"] = args.addr
        cronjob["spec"]["jobTemplate"]["spec"]["template"]["spec"]["env"][6]["value"] = f"https://{args.addr}:30442/auth/realms/react-keycloak/protocol/openid-connect/token"
    else:
        exit(1)

    if os.path.exists("./service.yaml"):
        with open("./service.yaml", "r") as f:
            service = yaml.safe_load(f)

        service["metadata"]["namespace"] = args.namespace
    else:
        exit(1)

    if os.path.exists("./secret.yaml"):
        with open("./secret.yaml", "r") as f:
            secret = yaml.safe_load(f)

        secret["metadata"]["namespace"] = args.namespace
    else:
        exit(1)
    

    try:
        core_v1_api.create_namespaced_secret(namespace=args.namespace, body=secret)
        apps_v1_api.create_namespaced_deployment(namespace=args.namespace, body=deployment)
        core_v1_api.create_namespaced_service(namespace=args.namespace, body=service)
    except ApiException:
        try:
            core_v1_api.delete_namespaced_service(namespace=args.namespace, name=service["metadata"]["name"])
            apps_v1_api.delete_namespaced_deployment(namespace=args.namespace, name=deployment["metadata"]["name"])
            core_v1_api.delete_namespaced_secret(namespace=args.namespace, name=secret["metadata"]["name"])
            exit(1)
        except ApiException:
            exit(1)


if __name__ == '__main__':
    main()
