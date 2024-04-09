import os
import yaml
import base64
import argparse
from kubernetes import client, config
from kubernetes.client.rest import ApiException

parser = argparse.ArgumentParser()

parser.add_argument("-a", "--minio_access_key", type=str, help="Endpoint for minio to save the models!", required=True)
parser.add_argument("-e", "--minio_endpoint", type=str, help="Access key for minio deployment!", required=True)
parser.add_argument("-l", "--local", type=str, help="Local IP address!", required=True)
parser.add_argument("-n", "--namespace", type=str, help="Namespace to run the files on!", required=True)
parser.add_argument("-s", "--minio_secret_key", type=str, help="Secret key for minio deployment!", required=True)

args = parser.parse_args()

def main():
    config.load_config()
    apps_v1_api = client.AppsV1Api()
    core_v1_api = client.CoreV1Api()

    if os.path.exists("./deployment.yaml"):
        with open("./deployment.yaml", "r") as f:
            deployment = yaml.safe_load(f)

        deployment["metadata"]["namespace"] = args.namespace
        deployment["spec"]["template"]["spec"]["containers"][0]["env"][0]["value"] = args.minio_endpoint
        deployment["spec"]["template"]["spec"]["containers"][0]["env"][2]["value"] = args.minio_access_key
        deployment["spec"]["template"]["spec"]["containers"][0]["env"][3]["value"] = args.minio_secret_key
        deployment["spec"]["template"]["spec"]["containers"][0]["image"] = deployment["spec"]["template"]["spec"]["containers"][0]["image"] + ":" + args.os
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

        encoded_bytes = base64.b64encode(args.encoded_minio_endpoint.encode('utf-8'))
        encoded_minio_endpoint = encoded_bytes.decode('utf-8')
        secret["data"]["mlflow_s3_endpoint_url"] = encoded_minio_endpoint

        encoded_bytes = base64.b64encode(args.minio_access_key.encode('utf-8'))
        encoded_minio_access_key = encoded_bytes.decode('utf-8')
        secret["data"]["aws_access_key_id"] = encoded_minio_access_key

        encoded_bytes = base64.b64encode(args.minio_secret_key.encode('utf-8'))
        encoded_minio_secret_key = encoded_bytes.decode('utf-8')
        secret["data"]["aws_secret_access_key"] = encoded_minio_secret_key

        encoded_bytes = base64.b64encode(f"http://{args.local}:31100".encode('utf-8'))
        encoded_mlflow_tracking_uri = encoded_bytes.decode('utf-8')
        secret["data"]["aws_secret_access_key"] = encoded_mlflow_tracking_uri
    else:
        exit(1)

    try:
        apps_v1_api.create_namespaced_deployment(namespace=args.namespace, body=deployment)
        core_v1_api.create_namespaced_service(namespace=args.namespace, body=service)
        core_v1_api.create_namespaced_secret(namespace=args.namespace, body=secret)
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
