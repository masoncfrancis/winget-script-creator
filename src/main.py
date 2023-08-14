# This program was written by ChatGPT

import os
import argparse

def main():
    parser = argparse.ArgumentParser(description="Generate PowerShell script and use winget based on input.")
    parser.add_argument("-a", "--add", metavar="filename", help="Add program names from a text file and generate a new script")
    parser.add_argument("-s", "--script", metavar="filename", help="Generate a script based on a text file")

    args = parser.parse_args()

    if args.add:
        add_programs_from_file(args.add)
    elif args.script:
        generate_powershell_script_from_file(args.script)
    else:
        interactive_input()

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

def generate_powershell_script_from_file(filename):
    program_list = []
    with open(filename, "r") as file:
        for line in file:
            program_name = line.strip()
            if program_name:
                program_list.append(program_name)
    if program_list:
        generate_powershell_script(program_list)
        print("PowerShell script has been generated based on the provided program list.")

def interactive_input():
    program_list = []

    while True:
        program_name = input("Enter the name of a program (or press Enter to finish): ")
        if not program_name:
            break
        program_list.append(program_name)
        with open("./out/winget_list.txt", "a") as file:
            file.write(program_name + "\n")

    if program_list:
        generate_powershell_script(program_list)
        print("PowerShell script and winget list have been generated in the 'out' directory.")

def generate_powershell_script(program_list):
    script_path = "./out/install_apps.ps1"

    with open(script_path, "w") as script_file:
        script_file.write("$programs = @(\n")
        for program in program_list:
            script_file.write(f'    "{program}",\n')
        script_file.write(")\n\n")
        script_file.write("foreach ($app in $programs) {\n")
        script_file.write("    Start-Process -Wait -FilePath 'winget' -ArgumentList 'install', $app\n")
        script_file.write("}\n")

if __name__ == "__main__":
    os.makedirs("./out", exist_ok=True)
    main()
