
import yaml
import argparse
from pathlib import Path
from kubernetes import client, config
from kubernetes.client.rest import ApiException

parser = argparse.ArgumentParser()

parser.add_argument("-n", "--namespace", type=str, help="Namespace to run the files on!", required=True)

args = parser.parse_args()

def run_service_account(path: str):
    config.load_config()
    core_v1_api = client.CoreV1Api()

    with open(path, "r") as f:
        service_account = yaml.safe_load(f)
        service_account["metadata"]["namespace"] = args.namespace

    try:
        core_v1_api.create_namespaced_service_account(namespace=args.namespace, body=service_account)
        return True
    except ApiException:
        return False


def main():
    error_counter = 0
    for path in Path("./").glob("*.yaml"):
        result = run_service_account(path)
        if not result:
            error_counter += 1
    
    if error_counter > 0:
        exit(error_counter)


if __name__ == '__main__':
    main()
