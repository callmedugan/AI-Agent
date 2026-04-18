from functions.get_file_content import *
from functions.get_files_info import *
from functions.run_python_file import *
from functions.write_file import *
from google.genai import types

# available functions
available_functions = types.Tool(
function_declarations=[
    schema_get_file_content,
    schema_get_files_info,
    schema_run_python_file,
    schema_write_file
    ],
)

# maps the function name string to the actual functions
function_map = {
    "get_file_content": get_file_content,
    "get_files_info": get_files_info,
    "run_python_file": run_python_file,
    "write_file": write_file,
}

#called by LLM - will pass in one of the available functions and return the result (takes types.functioncall obj)
def call_function(function_call, verbose=False):
    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")

    # ensure we have either a name or empty string to pass into the dict
    function_name = function_call.name or ""

    # return an error in the form of types.content tool for the LLM
    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    
    # make a shallow copy of the args passed into function_call
    args = dict(function_call.args) if function_call.args else {}

    # set our working directory
    args["working_directory"] = "./calculator"

    # call the function by looking up the name in the dict passing in args
    function_result = function_map[function_name](**args)

    # return a useful result in the form of a content for the LLM
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )
    


    
