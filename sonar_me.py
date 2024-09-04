import os
import sys
import json
import argparse
from config import AppConfig


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
    "--config",
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
    default=AppConfig.DEFAULT_DOCKERFILE_NAME
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
TEMPLATE_FILE = args.template
EXCLUDED = list(args.exclude)

if not os.path.exists(FOLDER):
    parser.error(f"Folder {FOLDER} is not found!")

config = {}

if os.path.exists(CONF_FILE):
    f = open(CONF_FILE, "r", encoding="utf-8")
    config = json.load(f)

app_key = config.setdefault(AppConfig.KEY_APP_KEY, args.key)
if app_key is None:
    parser.error("App key must be set as argument or in config file!")

app_token = config.setdefault(AppConfig.KEY_APP_TOKEN, args.token)
if app_token is None:
    parser.error("App token must be set as argument or in config file!")

host = config.setdefault(AppConfig.KEY_SONAR_HOST, args.host)
if host is None:
    parser.error("Sonarqube host must be set as argument or in config file!")

port = config.setdefault(AppConfig.KEY_SONAR_PORT, args.port)
if port is None:
    config[AppConfig.KEY_SONAR_PORT] = AppConfig.DEFAULT_SONAR_PORT

if args.dockerfile_name != AppConfig.DEFAULT_DOCKERFILE_NAME:
    config[AppConfig.KEY_DOCKERFILE_NAME] = args.dockerfile_name

if args.save_image:
    config[AppConfig.KEY_DELETE_IMAGE] = True

if args.save_dockerfile:
    config[AppConfig.KEY_DELETE_DOCKERFILE] = True

conf_excludes: list = config.setdefault(AppConfig.KEY_EXCLUDE, list())
conf_excludes.extend(EXCLUDED)

appConfig = AppConfig(config)

# open template file and get all the data
f = open(TEMPLATE_FILE, "r", encoding="utf-8")
TEMPLATE = f.read()
f.close()

# Changing cwd to work with project files
os.chdir(FOLDER)

with open(appConfig.dockerfile_name, "w", encoding="utf-8") as dockerfile:
    template_data = appConfig.data
    template_data["coverage_exclude"] = ",".join(appConfig.exclude) if len(appConfig.exclude) > 0 else "NONE"
    formatted_template = TEMPLATE.format(**template_data)
    dockerfile.write(formatted_template)

# Start build image
IMAGE_NAME = f"sonarme-{os.path.basename(FOLDER).lower()}"

code = os.system(f"docker build -f {appConfig.dockerfile_name} -t {IMAGE_NAME} . --no-cache")
# Cleanup
if appConfig.delete_image:
    os.system(f"docker rmi {IMAGE_NAME}")

if appConfig.delete_dockerfile:
    os.remove(appConfig.dockerfile_name)
