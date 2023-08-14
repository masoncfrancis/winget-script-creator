# This program was written by ChatGPT and Mason Francis

import os
import argparse

def main():
    parser = argparse.ArgumentParser(description="Generate PowerShell script and use winget based on input.")
    parser.add_argument("-a", "--add", metavar="filename", help="Add program names to an existing text file and generate a new script")
    parser.add_argument("-s", "--script", metavar="filename", help="Generate a script based on an text file")
    parser.add_argument("-n", "--new", action="store_true", help="Interactive mode to manually enter program names")
    parser.add_argument("-o", "--output", metavar="filename", default="install_apps.ps1", help="Specify the output filename for the PowerShell script")

    args = parser.parse_args()

    if args.add:
        add_programs_from_file(args.add)
    elif args.script:
        generate_powershell_script_from_file(args.script, args.output)
    elif args.new:
        interactive_input(args.output)
    else:
        parser.print_usage()

def add_programs_from_file(filename):
    program_list = []
    with open(filename, "r") as file:
        for line in file:
            program_name = line.strip()
            if program_name:
                program_list.append(program_name)
    if program_list:
        generate_powershell_script(program_list)
        print("PowerShell script has been generated based on the added programs.")

def generate_powershell_script_from_file(filename, output_filename):
    program_list = []
    with open(filename, "r") as file:
        for line in file:
            program_name = line.strip()
            if program_name:
                program_list.append(program_name)
    if program_list:
        generate_powershell_script(program_list, output_filename)
        print(f"PowerShell script '{output_filename}' has been generated based on the provided program list.")

def interactive_input(output_filename):
    program_list = []

    while True:
        program_name = input("Enter the name of a program (or press Enter to finish): ")
        if not program_name:
            break
        program_list.append(program_name)
        with open("winget_list.txt", "a") as file:
            file.write(program_name + "\n")

    if program_list:
        generate_powershell_script(program_list, output_filename)
        print(f"PowerShell script '{output_filename}' and winget list have been generated in the current directory.")

def generate_powershell_script(program_list, output_filename=None):
    if not output_filename:
        output_filename = "install_apps.ps1"
    with open(output_filename, "w") as script_file:
        script_file.write("$programs = @(\n")
        for program in program_list:
            script_file.write(f'    "{program}",\n')
        script_file.write(")\n\n")
        script_file.write("foreach ($app in $programs) {\n")
        script_file.write("    Start-Process -Wait -FilePath 'winget' -ArgumentList 'install', $app\n")
        script_file.write("}\n")

if __name__ == "__main__":
    main()
