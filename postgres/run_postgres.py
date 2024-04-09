import os
import yaml
import base64
import argparse
from kubernetes import client, config
from kubernetes.client.rest import ApiException

parser = argparse.ArgumentParser()

parser.add_argument("-a", "--addr", type=str, help="Address for deploymnets db!", required=True)
parser.add_argument("-n", "--namespace", type=str, help="Namespace to run the deployment on!", required=True)
parser.add_argument("-u", "--username", type=str, help="Current Logged in user!", required=True)

args = parser.parse_args()

def main():
    config.load_config()
    apps_v1_api = client.AppsV1Api()
    core_v1_api = client.CoreV1Api()

    if os.path.exists("./deployment.yaml"):
        with open("./deployment.yaml", "r") as f:
            deployment = yaml.safe_load(f)

        deployment["metadata"]["namespace"] = args.namespace
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

        encoded_bytes = base64.b64encode(args.addr.encode('utf-8'))
        encoded_host = encoded_bytes.decode('utf-8')
        secret["data"]["host"] = encoded_host
    else:
        exit(1)

    if os.path.exists("./pv-volume.yaml"):
        with open("./pv-volume..yaml", "r") as f:
            pv_volume = yaml.safe_load(f)

        pv_volume["metadata"]["namespace"] = args.namespace
        pv_volume["spec"]["hostPath"]["path"] = f"/home/{args.username}/postgres_data"
    else:
        exit(1)

    if os.path.exists("./pv-claim.yaml"):
        with open("./pv-claim.yaml", "r") as f:
            pv_claim = yaml.safe_load(f)

        pv_claim["metadata"]["namespace"] = args.namespace
    else:
        exit(1)
    

    try:
        core_v1_api.create_namespaced_secret(namespace=args.namespace, body=secret)
        apps_v1_api.create_namespaced_deployment(namespace=args.namespace, body=deployment)
        core_v1_api.create_namespaced_service(namespace=args.namespace, body=service)
        core_v1_api.create_namespaced_persistent_volume_claim(namespace=args.namespace, body=pv_claim)
        core_v1_api.create_persistent_volume(body=pv_volume)
    except ApiException:
        try:
            core_v1_api.delete_namespaced_service(namespace=args.namespace, name=service["metadata"]["name"])
            apps_v1_api.delete_namespaced_deployment(namespace=args.namespace, name=deployment["metadata"]["name"])
            core_v1_api.delete_namespaced_secret(namespace=args.namespace, name=secret["metadata"]["name"])
            core_v1_api.delete_namespaced_persistent_volume_claim(namespace=args.namespace, name=pv_claim["metadata"]["name"])
            core_v1_api.delete_persistent_volume(name=pv_volume["metadata"]["name"])
            exit(1)
        except ApiException:
            exit(1)


if __name__ == '__main__':
    main()
