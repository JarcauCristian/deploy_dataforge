import json
import shlex
import subprocess
from pathlib import Path
from time import sleep


def deploy(path: str, **kwargs):
    quoted_args = []
    
    for value in kwargs.values():
        quoted_args.append(shlex.quote(str(value)))

    command = [str(path), *quoted_args]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.returncode, result.stdout, result.stderr


def undeploy(path: str, **kwargs):
    quoted_args = []
    
    for value in kwargs.values():
        quoted_args.append(shlex.quote(str(value)))

    command = [str(path), *quoted_args]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.returncode, result.stdout, result.stderr


def make_executable(path: str):
    result = subprocess.run(["chmod", "+x", str(path)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.returncode, result.stdout, result.stderr


def load_config(path: str):
    with open(path, "r") as f:
        config = json.loads(f.read())
    
    return config


def main():
    config = load_config("./config.json")

    for path in Path.cwd().rglob("*.sh"):
        make_executable(path)

    failed_deployments = []
    for path in Path.cwd().rglob("deploy_*.sh"):
        deployment = str(path).split("/")[-2]
        print(f"Deploying {deployment}")
        if config[deployment].get("wait_time") is None:
            result = deploy(path, **{"namespace": config["namespace"]} | config[deployment]["values"]) if config[deployment].get("values") is not None else deploy(path, **{"namespace": config["namespace"]})
        else:
            result = deploy(path, **{"namespace": config["namespace"]} | config[deployment]["values"]) if config[deployment].get("values") is not None else deploy(path, **{"namespace": config["namespace"]})
            sleep(config[deployment]["wait_time"])

        if result[0] > 0:
            print(f"Could not create {deployment}: {result[0]}, {result[1]}, {result[2]}")
            failed_deployments.append(deployment)
    
    for path in Path.cwd().rglob("undeploy_*.sh"):
        deployment = str(path).split("/")[-2]
        if deployment in failed_deployments:
            undeploy(path, **{"namespace": config["namespace"]})


if __name__ == "__main__":
    main()

