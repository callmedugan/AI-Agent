import os
from google.genai import types

def write_file(working_directory, file_path, content):

    #make sure the file path is inside our specified working directory so AI doesnt go to the no-no places
    working_dir_abs = os.path.abspath(working_directory)
    file_path_abs = os.path.normpath(os.path.join(working_dir_abs, file_path))
    # Will be True or False if directory is valid and file inside the working directory
    file_is_in_dir = os.path.commonpath([working_dir_abs, file_path_abs]) == working_dir_abs
    if not file_is_in_dir:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if os.path.isdir(file_path_abs):
        return f'Error: Cannot write to "{file_path}" as it is a directory'
    
    #create any needed directories from the passed in file_path
    file_path_parent_dir = os.path.dirname(file_path_abs)
    os.makedirs(file_path_parent_dir, exist_ok=True)

    #open file and write
    try:
        with open(file_path_abs, "w") as f:
            f.write(content)
    except:
        return f'Error: Failed to write contents to: "{file_path}"'


    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'    

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description=f"Writes content to a file in a specified directory relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path", "content"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Target directory path and file name to be written to, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content as a string to be written to the specified file (file_path)",
            ),
        },
    ),
)