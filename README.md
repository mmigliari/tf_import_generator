## Terraform Import Command Generator

This project helps you generate Terraform import commands from a Terraform state file.  It can handle resources in root and child modules, as well as resources using count and for_each declarations.

### Requirements
- Python 3.x

### Usage
1. Make the script executable:
    ```
    chmod +x tf_import_generator.py
    ```
3. Run the script with the path to your Terraform state file:
    ```
    ./tf_import_generator.py /path/to/your/terraform.tfstate
    ```
    By default, the generated import commands will be saved to a file called `import_commands.txt`. If you want to save the commands to a different file, use the `--output` option:
    ```
    ./tf_import_generator.py /path/to/your/terraform.tfstate --output my_import_commands.txt
    ```
The script will generate Terraform import commands based on the resources found in the state file and print them to the console. It will also save the commands to the specified output file.

Review the generated import commands and execute them as needed using your terminal or command prompt.

Enjoy!