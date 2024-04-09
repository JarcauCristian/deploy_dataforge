import os
import yaml
import argparse
from kubernetes import client, config
from kubernetes.client.rest import ApiException

parser = argparse.ArgumentParser()

parser.add_argument("-n", "--namespace", type=str, help="Namespace to run the deployment on!", required=True)
parser.add_argument("-o", "--os", type=str, help="Os for image tag!", required=True)

args = parser.parse_args()

def main():
    config.load_config()
    apps_v1_api = client.AppsV1Api()
    core_v1_api = client.CoreV1Api()
    networking_v1_api = client.NetworkingV1Api()

    if os.path.exists("./deployment.yaml"):
        with open("./deployment.yaml", "r") as f:
            deployment = yaml.safe_load(f)

        deployment["spec"]["template"]["spec"]["containers"][0]["image"] = deployment["spec"]["template"]["spec"]["containers"][0]["image"] + ":" + args.os
        deployment["metadata"]["namespace"] = args.namespace
    else:
        exit(1)

    if os.path.exists("./service.yaml"):
        with open("./service.yaml", "r") as f:
            service = yaml.safe_load(f)

        service["metadata"]["namespace"] = args.namespace
    else:
        exit(1)

    if os.path.exists("./ingress.yaml"):
        with open("./ingress.yaml", "r") as f:
            ingress = yaml.safe_load(f)

        ingress["metadata"]["namespace"] = args.namespace
    else:
        exit(1)
    

    try:
        apps_v1_api.create_namespaced_deployment(namespace=args.namespace, body=deployment)
        core_v1_api.create_namespaced_service(namespace=args.namespace, body=service)
        networking_v1_api.create_namespaced_ingress(namespace=args.namespace, body=ingress)
    except ApiException:
        try:
            core_v1_api.delete_namespaced_service(namespace=args.namespace, name=service["metadata"]["name"])
            apps_v1_api.delete_namespaced_deployment(namespace=args.namespace, name=deployment["metadata"]["name"])
            networking_v1_api.delete_namespaced_ingress(namespace=args.namespace, name=ingress["metadata"]["name"])
            exit(1)
        except ApiException:
            exit(1)


if __name__ == '__main__':
    main()
