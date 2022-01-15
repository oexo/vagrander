import os
from pathlib import Path
import jsonschema
from jsonschema import validate
import yaml
from jinja2 import Environment
from jinja2 import FileSystemLoader
import argparse
import vagrant

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
    parser.add_argument('action', metavar='N', type=str,
                        help='action for vagrant')
    parser.add_argument('vm', metavar='N', type=str,
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
    return 0


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


def act_vagrant(action, vm_path):

    # TODO: async

    v1 = vagrant.Vagrant(vm_path)

    vm_statuses = {
        "up": "running",
        "halt": "poweroff",
        "destroy": "not_created",
        "status": ""
    }
    
    vm_status = str(v1.status()[0][1])
    vm = vm_path[vm_path.rfind("/") + 1:]

    if action not in vm_statuses.keys():
        print(f"Invalid action {action.upper}!!")
        return 1
    elif action == 'status':
        print(f'VM {vm} in {vm_status.upper()} state')
    elif vm_statuses[action] == vm_status or action == 'halt' and vm_status != "running":
        print(f'VM {vm} already in {vm_status.upper()} state')
    else:
        print(f'Attempt to apply the action {action.upper()} to the VM {vm}')
        getattr(v1, action)()
        vm_status = str(v1.status()[0][1])
        if vm_statuses[action] == vm_status:
            print(f"Completed successfully")
        else:
            print(f"Error, VM {vm_path} in {vm_status} state")
            return 1

    return 0


def is_vm_exist(vm):
    for node in get_nodes_from_inventory():
        if node["hostname"] == vm:
            return True
    return False


def main():

    args = get_args()

    if args.vm == "all" or is_vm_exist(args.vm):
        update_dst_vfiles()
        if args.vm == "all":
            for vm in get_nodes_from_inventory():
                vm_path = VAGRANT_CATALOG + vm["hostname"]
                act_vagrant(args.action, vm_path)
        else:
            vm_path = VAGRANT_CATALOG + args.vm
            act_vagrant(args.action, vm_path)
    else:
        print("There is no suitable VM for actions")


if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
