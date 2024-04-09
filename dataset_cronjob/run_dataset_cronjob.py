import os
import yaml
import argparse
from kubernetes import client, config
from kubernetes.client.rest import ApiException

parser = argparse.ArgumentParser()

parser.add_argument("-a", "--addr", type=str, help="Address for postgres db!", required=True)
parser.add_argument("-o", "--os", type=str, help="Os for image tag!", required=True)
parser.add_argument("-n", "--namespace", type=str, help="Namespace to run the deployment on!", required=True)

args = parser.parse_args()

def main():
    config.load_config()
    batch_v1_api = client.BatchV1Api()
    core_v1_api = client.CoreV1Api()

    if os.path.exists("./deployment.yaml"):
        with open("./deployment.yaml", "r") as f:
            cronjob = yaml.safe_load(f)

        cronjob["spec"]["jobTemplate"]["spec"]["template"]["spec"]["containers"][0]["env"][6]["value"] = f"https://{args.addr}:30442/auth/realms/react-keycloak/protocol/openid-connect/userinfo"
        cronjob["spec"]["jobTemplate"]["spec"]["template"]["spec"]["containers"][0]["env"][9]["value"] = args.namespace
        cronjob["spec"]["jobTemplate"]["spec"]["template"]["spec"]["containers"][0]["image"] = cronjob["spec"]["jobTemplate"]["spec"]["template"]["spec"]["containers"][0]["image"]  + ":" + args.os
        cronjob["metadata"]["namespace"] = args.namespace
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
        batch_v1_api.create_namespaced_cron_job(namespace=args.namespace, body=cronjob)
    except ApiException:
        try:
            batch_v1_api.delete_namespaced_cron_job(namespace=args.namespace, name=cronjob["metadata"]["name"])
            core_v1_api.delete_namespaced_secret(namespace=args.namespace, body=secret["metadata"]["name"])
            exit(1)
        except ApiException:
            exit(1)


if __name__ == '__main__':
    main()
