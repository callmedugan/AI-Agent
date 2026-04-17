import os
from dotenv import load_dotenv
from google import genai

def main():

    #loading api key
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("api key not found")
    
    #creating gen ai client
    client = genai.Client(api_key=api_key)

    content = client.models.generate_content(model="gemini-2.5-flash", contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.")
    
    print(content.text)


if __name__ == "__main__":
    main()
