import os
import sys
import json
import argparse

import const
import helpers

parser = argparse.ArgumentParser(
    prog="SonarME.NET",
    description="CLI tool for quick setup your .NET project to scan with SonarQube using Docker image",
    epilog="Have a good day!"
)

parser.add_argument(
    "folder",
    help="Path to .net project folder"
)

parser.add_argument(
    "--key", "-k",
    help="App key in sonarqube",
    default=None
)

parser.add_argument(
    "--token", "-t",
    help="Sonarqube auth token for app_key",
    default=None
)

parser.add_argument(
    "--config", "-c",
    help="Specify path to configfile",
    default="config.json"
)

parser.add_argument(
    "--template",
    help="Specify path to dockerfile template",
    default="dockerfile_template"
)

parser.add_argument(
    "--exclude", "-exc",
    help="Add files and folder to exclude from test coverage",
    action="append",
    nargs="*",
    default=list()
)

parser.add_argument(
    "--host",
    help="Specify the sonarqube host address",
    default=None
)

parser.add_argument(
    "--port",
    help="Specify the port for sonarqube",
    default=None
)

parser.add_argument(
    "--dockerfile-name", "-dfn",
    help="Specify the name of dockerfile that will be created inside project",
    default=const.DEFAULT_DOCKERFILE_NAME
)

parser.add_argument(
    "--save-image", "-si",
    help="Specify that image should be not deleted after the process",
    action="store_false"
)

parser.add_argument(
    "--save-dockerfile", "-sd",
    help="Specify that dockerfile should not be deleted after the process",
    action="store_false"
)

args = parser.parse_args()
APP_WORK_DIR = os.getcwd()

FOLDER = args.folder
CONF_FILE = args.config
TEMPLATE_FILE = os.path.abspath(args.template)
EXCLUDED = list(args.exclude)

if not os.path.exists(FOLDER):
    parser.error(f"Folder {FOLDER} is not found!")

config = helpers.from_json_file(CONF_FILE)

app_key = config.setdefault(const.KEY_APP_KEY, args.key)
if app_key is None:
    parser.error("App key must be set as argument or in config file!")

app_token = config.setdefault(const.KEY_APP_TOKEN, args.token)
if app_token is None:
    parser.error("App token must be set as argument or in config file!")

host = config.setdefault(const.KEY_SONAR_HOST, args.host)
if host is None:
    parser.error("Sonarqube host must be set as argument or in config file!")

port = config.setdefault(const.KEY_SONAR_PORT, args.port)
if port is None:
    config[const.KEY_SONAR_PORT] = const.DEFAULT_SONAR_PORT

if args.dockerfile_name != const.DEFAULT_DOCKERFILE_NAME or const.KEY_DOCKERFILE_NAME not in config:
    config[const.KEY_DOCKERFILE_NAME] = args.dockerfile_name

if args.save_image:
    config[const.KEY_DELETE_IMAGE] = True

if args.save_dockerfile:
    config[const.KEY_DELETE_DOCKERFILE] = True

conf_excludes: list = config.setdefault(const.KEY_EXCLUDE, list())
conf_excludes.extend(EXCLUDED)

os.chdir(FOLDER)
helpers.generate_template(TEMPLATE_FILE, config[const.KEY_DOCKERFILE_NAME], config)

# Start build image
IMAGE_NAME = f"sonarme-{os.path.basename(FOLDER).lower()}"

code = os.system(f"docker build -f {config[const.KEY_DOCKERFILE_NAME]} -t {IMAGE_NAME} . --no-cache")
# Cleanup
if config[const.KEY_DELETE_IMAGE]:
    os.system(f"docker rmi {IMAGE_NAME}")

if config[const.KEY_DELETE_DOCKERFILE]:
    os.remove(config[const.KEY_DOCKERFILE_NAME])
