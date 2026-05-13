from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
from pathlib import Path
import mimetypes

MODEL_NAME='gemini-2.5-flash'
SYSTEM_PROMPT = 'systemPrompt.md'

load_dotenv()


def main():
    llm_loop()


def llm_loop():
    print("Welcome. I am and expert legal. Use Following commands:")
    print(get_commands())
    api_key = os.getenv("GOOGLE_GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    history = []
    #encoding = tiktoken.encoding_for_model(MODEL_NAME)
    isInDraftEditMode=False
    history=[]
    while 1==1:
        userCommand = input("You > \n")
        if userCommand =="#new":
            if len(history)>2:
                add_memory(client,history)
            isInDraftEditMode=False
            history.clear()
            fileName = input("File name > \n")
            new_file_context = ("Here is a new document." 
                               "Process this according to the Senior Digital Associate protocol." 
                               "Focus specifically on the Case Fact Summary")
            fileFullPath="./legalDocs/"+fileName
            response = call_llm_with_file(client, new_file_context, fileFullPath)
            print("Me > \n" + response.text)
            isInDraftEditMode =True
            history.append("{role= user, content="+new_file_context +"}")
            history.append("{role= assistant, content="+response.text +"}")
            
        if isInDraftEditMode:
            context ="\n".join(history)
            response = call_llm(client, context)
            print("Me > \n" + response.text)
        else:
            print(get_commands())



def add_memory(client, history):
     context ="###Input\n".join(history)
     context += ("###Description"
                 "Input is chat history between you and user. It contains users edits on your draft generation."
                 "###Output"
                 "Analyze the difference between your draft and the operator's version. Create summary."
                 "It will be added to your system prompt. So that you don't make same mistakes and can remember user preference")
     response = call_llm(client,context)
     file_path=Path(SYSTEM_PROMPT)
     with file_path.open("SYSTEM_PROMPT") as file:
        file.write(context)

def call_llm(client, context):
    response = client.models.generate_content(
            model=MODEL_NAME,
            contents={'text': context},
            config=get_llm_config()
            )
    return response

def call_llm_with_file(client, context, file):
    file_path = Path(file)
    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type:
        mime_type = "application/octet-stream"
    response = client.models.generate_content(
            model=MODEL_NAME,
            contents=[
                types.Part.from_bytes(
                    data=file_path.read_bytes(),
                    mime_type=mime_type
                ),
                context
                ],
            config=get_llm_config()
            )
    return response
                        

def get_llm_config():
    return {
                'temperature': 0.5,
                'top_p': 0.95,
                'top_k': 20,
                'system_instruction': get_system_instruction()
                }
            
def get_system_instruction():
    content = Path(SYSTEM_PROMPT).read_text()
    return content


def get_commands():
    commands=(
        "1. Type <#new> to start a new document draft sesstion"
        "2. Type <#exit> to shut me down"
    )
    return commands



if __name__ == "__main__":
    main()
