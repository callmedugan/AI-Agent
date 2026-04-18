import os, sys, time, argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function
from config import MAX_CALLS_PER_PROMPT

def main():

    #loading api key
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("api key not found")
    
    #creating gen ai client
    client = genai.Client(api_key=api_key)

    # get user input
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output") #toggle on for detailed info in the output
    args = parser.parse_args() #args.user_prompt

    # store messages
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    #api call
    for _ in range(MAX_CALLS_PER_PROMPT):
        response = None
        #try 10 times 2 secs in between for when there is a lot of traffic
        for attempt in range(10):
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=messages,
                    config=types.GenerateContentConfig(
                        tools=[available_functions], #from call_function.py
                        system_instruction=system_prompt #from prompts.py
                        )
                    )
                # check candidates and add the content to messages
                if not response.candidates:
                    raise Exception("failed to return candidates from last call")
                for c in response.candidates:
                    messages.append(c.content)
                # break out when response received
                break
            except Exception as e:
                if attempt == 2:
                    raise RuntimeError("failed api initial call after 10 tries") from e
                time.sleep(2)
            

        #usage metadata
        if response is None or response.usage_metadata is None:
            raise RuntimeError("failed api call, cannot access metadata")
        prompt_tokens = response.usage_metadata.prompt_token_count
        response_tokens = response.usage_metadata.candidates_token_count

        # printing the verbose info
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {prompt_tokens}")
            print(f"Response tokens: {response_tokens}")

        #normal response
        print("Response:")

        # loop through function calls returned from the LLM and run the functions 
        if response.function_calls:
            for call in response.function_calls:
                #print(f"Calling function: {call.name}({call.args})")
                function_call_result = call_function(call)
                # if no results
                if not function_call_result.parts:
                    raise Exception(f"{call} returned no results (function_call_result.parts empty)")
                if not function_call_result.parts[0].function_response:
                    raise Exception(f"{call} returned no results (function_call_result.parts[0].function_response is None)")
                if not function_call_result.parts[0].function_response.response:
                    raise Exception(f"{call} returned no results (function_call_result.parts[0].function_response.response is None)")
                # finally if we get something back add to messages:
                messages.append(types.Content(role="user", parts=function_call_result.parts))
                # verbose
                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
        else:
            # no more function calls so we must be done
            print(response.text)
            return
        
    #if agent does not find a final response under max attempts then return error
    print(f"ERROR: Was not able to produce a final response in under {MAX_CALLS_PER_PROMPT} calls.")
    sys.exit(1)

if __name__ == "__main__":
    main()
