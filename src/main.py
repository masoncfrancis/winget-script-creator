# This program was written by ChatGPT

import os

def main():
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
    winget_list_path = "./out/winget_list.txt"
    
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
