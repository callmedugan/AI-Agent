import os
from config import MAX_FILE_READ_BYTES
from google.genai import types

def get_file_content(working_directory, file_path):
        
    #make sure the file path is inside our specified working directory so AI doesnt go to the no-no places
    working_dir_abs = os.path.abspath(working_directory)
    file_path_abs = os.path.normpath(os.path.join(working_dir_abs, file_path))
    # Will be True or False if directory is valid and file inside the working directory
    file_is_in_dir = os.path.commonpath([working_dir_abs, file_path_abs]) == working_dir_abs
    if not file_is_in_dir:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(file_path_abs):
        return f'Error: File not found or is not a regular file: "{file_path} in {working_directory}"'
    
    #do the actual reading
    try:
        # Check to see if the file is longer than the allotted read bytes (dont want to use up a ton of tokens)
        with open(file_path_abs, "r") as f:
            file_contents = f.read(MAX_FILE_READ_BYTES)
            if f.read(1):
                file_contents += f'[...File "{file_path}" truncated at {MAX_FILE_READ_BYTES} characters]'
    except:
        return f'Error: Failed to read contents of: "{file_path}"'
    
    return file_contents

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Reads a file in a specified directory relative to the working directory, returning up to {MAX_FILE_READ_BYTES} characters as string",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Directory path and file name, relative to the working directory",
            ),
        },
    ),
)