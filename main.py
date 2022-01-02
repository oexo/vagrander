import os
from pathlib import Path
import jsonschema
from jsonschema import validate
import yaml
import json

SCHEMA = {
    "type": "object",
    "required": ["nodes", "templates"]

}

VAGRANT_CATALOG = "/Users/dmitriygarbovskiy/Learning/vagrant/"
VAGRANT_TEMPLATE_NAME = "VTemplate.txt"
MAIN_DIR = os.path.dirname(os.path.realpath(__file__))

with open(Path(MAIN_DIR + "/" + "./inventory.yaml"), "r") as inventory:
    INVENTORY = yaml.safe_load(inventory)


def open_template_file(catalog=VAGRANT_CATALOG, file=VAGRANT_TEMPLATE_NAME):
    with open(catalog + file, "r") as vagrant_template_file:
        return vagrant_template_file.read()
    # TODO: переделать вагранд-файл в шаблон j2


def create_vagrant_from_template(hostname, ip):
    print("hello world")
    #TODO: проработать структура инвентори-файла (должен быть like as ансибл)
    #TODO: компилировать вагрант-файл на основе шаблона и инвентори


def validate_inventory(inventory):
    validate(inventory, yaml.safe_load(SCHEMA))


def is_json_valid(json_data: dict, json_schema: dict) -> bool:
    """
    Func for validate json by the python module jsonschema
    :param json_data: Dictionary for confirmation
    :param json_schema: Confirmation scheme
    :return: Bool, The True if the dict is valid, and False if not.
    """
    try:
        validate(instance=json_data, schema=json_schema)
    except jsonschema.exceptions.ValidationError as err:
        return False
    return True


def main():
    # for data in INVENTORY:
    #     print(INVENTORY[data])

    print(INVENTORY)
    print(is_json_valid(INVENTORY, SCHEMA))


if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
