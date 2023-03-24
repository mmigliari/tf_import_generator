#!/usr/bin/env python3

import argparse
import json
import os


def read_terraform_state_file(file_path):
    with open(file_path, "r") as file:
        return json.load(file)


def generate_import_commands(state_data):
    import_commands = []
    if "resources" in state_data:
        resources = state_data["resources"]
        process_resources(resources, import_commands)
    return import_commands


def process_resources(resources, import_commands, module_path=None):
    for resource in resources:
        provider = resource["provider"]
        resource_type = resource["type"]
        resource_name = resource["name"]
        instances = resource["instances"]

        module = resource.get("module")
        if module:
            resource_address = f"{module}.{resource_type}.{resource_name}"
        elif module_path:
            resource_address = f"{module_path}.{resource_type}.{resource_name}"
        else:
            resource_address = f"{resource_type}.{resource_name}"

        for instance in instances:
            resource_id = instance["attributes"]["id"]

            if "index_key" in instance:
                index_key = instance["index_key"]
                if isinstance(index_key, int):
                    terraform_address = f"{resource_address}[{index_key}]"
                else:
                    terraform_address = f'{resource_address}["{index_key}"]'
            else:
                terraform_address = resource_address

            import_command = f"terraform import {terraform_address} {resource_id}"
            import_commands.append(import_command)

        if "child_modules" in resource:
            for child_module in resource["child_modules"]:
                child_module_path = (
                    f"{module_path}.{child_module['name']}"
                    if module_path
                    else child_module["name"]
                )
                process_resources(
                    child_module["resources"], import_commands, child_module_path
                )


def main():
    parser = argparse.ArgumentParser(
        description="Generate Terraform import commands from a Terraform state file."
    )
    parser.add_argument("state_file", help="Path to the Terraform state file")
    parser.add_argument(
        "--output",
        help="Output file for the generated import commands",
        default="import_commands.txt",
    )
    args = parser.parse_args()

    state_file = args.state_file
    output_file = args.output

    if not os.path.isfile(state_file):
        print(f"Error: {state_file} is not a valid file.")
        return

    state_data = read_terraform_state_file(state_file)
    import_commands = generate_import_commands(state_data)

    with open(output_file, "w") as file:
        for command in import_commands:
            file.write(f"{command}\n")
            print(command)

    print(f"\nGenerated import commands have been saved to {output_file}.")


if __name__ == "__main__":
    main()


