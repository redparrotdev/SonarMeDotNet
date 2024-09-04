# SonarMe .NET
A CLI tool to automate process of scanning .net project using Sonarqube.

## Quick start

Get code localy and use the tool.

## Usage

To run a tool you need a Sonarqube server run locally.
Create a project in Sonar, because you need a project key and token

```sh
sonar_me.py <path_fo_project_folder> --key <your_app_key> --token <your_app_token> --host <sonarqube_host_address>
```

_NOTE:_ Folder must contain .sln file

_NOTE:_ For host specify addres witout port, 9000 port is set as default

Additionaly you can specify `--exclude` option and add files and folder to exclude from sonar code coverage.

You also can use a `json`-file to save configuration for projects:

```json
{
    "app_key": "<your app key>",
    "app_token": "<your app token>",
    "sonar_host": "<your sonar host address>",
    "exclude": [
        "list",
        "of",
        "excludes"
    ],
    // To override port
    "sonar_port": 8080,
    // To override dockerfile name
    "dockerfile_name": "myname.dockerfile",
    // To keep dockerfile after run (will be deleted by default)
    "delete_dockerfile": false,
    // To keep image after run (will be deleted by default)
    "delete_image": false
}
```
and then use `--config` with path to config file
