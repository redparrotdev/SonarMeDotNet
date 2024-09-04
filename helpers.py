import os
import json
import const

def from_json_file(file_path, **options):
    config = {}
        
    if os.path.exists(file_path):
        config = json.load(open(file_path, "r", **options))

    return config

def transform_exclude(config: dict, join_string=","):
    config = config.copy()

    if const.KEY_EXCLUDE not in config and config[const.KEY_EXCLUDE] is not list:
        raise KeyError(const.KEY_EXCLUDE)
    
    key = const.KEY_EXCLUDE
    config[key] = join_string.join(config[key])

    return config


def generate_template(template_path: str, output_path: str, template_data: dict):
    # open template file and get all the data
    f = open(template_path, "r", encoding="utf-8")
    template = f.read()
    f.close()

    with open(output_path, "w", encoding="utf-8") as dockerfile:
        template_data = transform_exclude(template_data)
        formatted_template = template.format(**template_data)
        dockerfile.write(formatted_template)

