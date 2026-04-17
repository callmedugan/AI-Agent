import os

#should always return a string even if error for the LLM to read and understand
def get_files_info(working_directory, directory="."):

    #set up guardrails so to make sure the directory is never outside the working directory
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
    # Will be True or False if directory is valid and inside the working directory
    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
    if not valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'
    
    items = []

    try:
        for item in os.listdir(target_dir):
            file = target_dir + "/" + item
            size = os.path.getsize(file)
            is_dir = os.path.isdir(file)
            string = (f"- {item}: file_size={size} bytes, is_dir={is_dir}")
            items.append(string)
    except Exception:
        return f"Error: error when reading {file}" #for the LLM
    
    result = "\n".join(items)
    print(result)
    return result