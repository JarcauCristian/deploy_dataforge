import json
import shlex
import subprocess
from pathlib import Path


def deploy_single(path: str, **kwargs):
    quoted_args = []
    
    for value in kwargs.values():
        quoted_args.append(shlex.quote(str(value)))

    command = f"{path} " + " ".join(quoted_args)
    result = subprocess.run(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.returncode


def load_config(path: str):
    with open(path, "r") as f:
        config = json.loads(f.read())
    
    return config


def main():
    config = load_config("./config.json")
    single_deployments = ["interface", "keycloak", "minio", "neo4j_api", "nignx", "notebook_cronjob", "notebook_deletition", "notebook_manager", "postgres", "redis", "role_bindings", "roles", "services", "storage_load_balancer"]

    for path in Path.cwd().rglob("*.sh"):
        deployment = str(path).split("\\")[-2]
        if config[deployment].get("values") is None:
            print("Configuration", deployment)

if __name__ == "__main__":
    main()

