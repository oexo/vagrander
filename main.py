import os
from pathlib import Path
import jsonschema
from jsonschema import validate
import yaml
from jinja2 import Environment
from jinja2 import FileSystemLoader
import argparse
import vagrant
from vagrant_wrapper import up_vm, halt_vm, destroy_vm, status_vm

SCHEMA = {
    "type": "object",
    "required": ["nodes", "templates"]
}

VAGRANT_CATALOG = "/Users/dmitriygarbovskiy/Learning/vagrant/"
VAGRANT_TEMPLATE_NAME = "VTemplate.txt"
MAIN_DIR = os.path.dirname(os.path.realpath(__file__))
INVENTORY_FILENAME = "inventory.yaml"
TEMPLATE_FOLDER = "templates"
TEMPLATE_FILENAME = "template.j2"
J2_ENVIRONMENT = Environment(loader=FileSystemLoader(TEMPLATE_FOLDER), trim_blocks=True)

with open(Path(MAIN_DIR + "/" + INVENTORY_FILENAME), "r") as inventory:
    INVENTORY = yaml.safe_load(inventory)


def get_args():
    parser = argparse.ArgumentParser(description='Vagrant wrapper')
    parser.add_argument('action', metavar='N', type=str, nargs='+',
                        help='action for vagrant')
    parser.add_argument('vm', metavar='N', type=str, nargs='+',
                        help='vm name or "all"')

    return parser.parse_args()


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


def get_nodes_from_inventory(inventory=INVENTORY):
    n = None
    for nodes in inventory["nodes"]:
        yield nodes


def get_templates_from_inventory(inventory=INVENTORY):
    n = None
    for templates in inventory["templates"]:
        yield templates


def render_template(unit: dict, template=TEMPLATE_FILENAME, j2_env=J2_ENVIRONMENT):
    template = j2_env.get_template(template)

    rendered_template = template.render(hostname=unit["hostname"],
                                        internal_ip=unit["internal_ip"],
                                        external_ip=unit["external_ip"],
                                        memory=unit["memory"],
                                        cpu=unit["cpu"])

    return rendered_template


def create_empty_file(filename: Path):
    with open(filename, "w"):
        pass


def save_template_to_file(filename: Path, text):
    with open(filename, "w+") as template:
        template.write(text)


def create_folder(folder: Path):
    # try:
    os.mkdir(folder)
    # except:
    #     return False
    return True


def update_dst_vfiles():
    if is_json_valid(INVENTORY, SCHEMA):
        for node in get_nodes_from_inventory():
            vm_folder = VAGRANT_CATALOG + node["hostname"]
            vagrant_file = vm_folder + "/" + "Vagrantfile"
            if not os.path.exists(vm_folder):
                create_folder(Path(vm_folder))
            if not os.path.exists(vagrant_file):
                create_empty_file(Path(vagrant_file))
            save_template_to_file(Path(vagrant_file), render_template(node))
    else:
        print(f" Inventory file {Path(MAIN_DIR + '/' + INVENTORY_FILENAME)} is not valid")


def act_vagrant(action, vm):

    print(action)
    print(vm)
    vm_folder = Path(VAGRANT_CATALOG + "/" + vm)

    if action == "up":
        up_vm(vm_folder)
    elif action == "halt":
        halt_vm(vm_folder)
    elif action == "destroy":
        destroy_vm(vm_folder)
    elif action == "status":
        status_vm(vm_folder)


def main():

    args = get_args()

    print(args.action)
    print(args.vm)

    update_dst_vfiles()

    act_vagrant(args.action[0], args.vm[0])


if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
