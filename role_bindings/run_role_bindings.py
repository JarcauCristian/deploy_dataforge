
import yaml
import argparse
from pathlib import Path
from kubernetes import client, config
from kubernetes.client.rest import ApiException

parser = argparse.ArgumentParser()

parser.add_argument("-n", "--namespace", type=str, help="Namespace to run the files on!", required=True)

args = parser.parse_args()

def run_role_bindings(path: str):
    config.load_config()
    rbac_api = client.RbacAuthorizationV1Api()

    with open(path, "r") as f:
        role = yaml.safe_load(f)
        role["metadata"]["namespace"] = args.namespace
        role["subjects"][0]["namespace"] = args.namespace

    try:
        rbac_api.create_namespaced_role_binding(namespace=args.namespace, body=role)
        return True
    except ApiException:
        return False


def main():
    error_counter = 0
    for path in Path("./").glob("*.yaml"):
        result = run_role_bindings(path)
        if not result:
            error_counter += 1
    
    if error_counter > 0:
        exit(error_counter)


if __name__ == '__main__':
    main()
