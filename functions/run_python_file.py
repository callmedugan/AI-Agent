import os
import subprocess

def run_python_file(working_directory, file_path, args=None):

    #make sure the file path is inside our specified working directory so AI doesnt go to the no-no places
    working_dir_abs = os.path.abspath(working_directory)
    file_path_abs = os.path.normpath(os.path.join(working_dir_abs, file_path))
    # Will be True or False if directory is valid and file inside the working directory
    file_is_in_dir = os.path.commonpath([working_dir_abs, file_path_abs]) == working_dir_abs
    if not file_is_in_dir:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(file_path_abs):
        return f'Error: "{file_path}" does not exist or is not a regular file'
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file'
    
    #run it up
    command_string = ["python", file_path_abs]
    if args:
        command_string.extend(args)

    #run command, return output, set cwd, get results as text not bytes, timeout of 30 seconds
    try:
        process = subprocess.run(command_string, capture_output=True, cwd=working_directory, text=True, timeout=30)

        if process.stdout == "" and process.stderr == "":
            return "No output produced"
        
        result = ""
        if process.returncode != 0:
            result += f"Process exited with code {process.returncode}"
        if process.stdout:
            result += f"\nSTDOUT: {process.stdout}"
        if process.stderr:
            result += f"\nSTDERR: {process.stderr}"

        return result
    
    except Exception as e:
        return f"Error: executing Python file: {e}"
