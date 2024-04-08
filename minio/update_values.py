import os
import yaml
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-u", "--user", type=str, help="Username for minio deployment!", required=True)
parser.add_argument("-p", "--password", type=str, help="Password for minio deployment!", required=True)

args = parser.parse_args()

def main():
    if os.path.exists("./values.yaml"):
        with open("./values.yaml", "r") as f:
            yaml_file = yaml.safe_load(f)

        yaml_file["auth"]["rootUser"] = args.user
        yaml_file["auth"]["rootPassword"] = args.password

        with open("./values.yaml", "w") as f:
            f.write(yaml.safe_dump(yaml_file))

if __name__ == '__main__':
    main()
