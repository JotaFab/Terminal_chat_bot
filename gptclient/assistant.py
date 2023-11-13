import json
from gptclient.logs import log_to_file
import os
import click
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style

path = os.getcwd()

def create_assistant(client,session):
    try:
        assis_name = session.prompt("Enter the name of your assistant: \n")  
        
        assistant = client.beta.assistants.create(
            model="gpt-3.5-turbo-16k-0613",
            name=assis_name,
            description="I am an AI assistant specializing in terminal operations. I possess expertise in bash, python, and other shell scripting languages, with a focus on Debian-based instructions.",
            instructions="When required, I will provide alternative solutions in shell or python code. I will first present the code, followed by a detailed explanation. All provided code will include comments to clarify its functionality.",
            tools=[{"type": "code_interpreter"}],
        )
        print(f"Assistant created with id {assistant.id}")
        print(f"Assistant name: {assistant.name}")
        
        log_to_file("assistants", assistant)
        
        # append the assistant id to the assistant_id.txt file
        with open(f"{path}/logs/assistant_ids.txt", "a") as f:
            f.write(f"{assistant.id}\n")
        print(f"Assistant id {assistant.id} appended to assistant_ids.txt")
        
    except Exception as e:
        print(f"Error: {e}", 'light_red')
        exit(1)
    except KeyboardInterrupt:
        print(f"Keyboard Interrupt, Exiting...", 'light_red')
        exit(1)
    return
    

def get_assistant_ids():
    """make a list of assistant ids from the assistant_ids.txt file and order from last to first line 
    """
    with open(f"{path}/logs/assistant_ids.txt", "r") as f:
        assistant_ids = f.readlines()
        assistant_ids = [x.strip() for x in assistant_ids]
        assistant_ids.reverse()
    f.close()
    return assistant_ids
    
    

def sanitize_id(id):
    
    return ''.join(c for c in id if c.isprintable())

def retrieve_assistant(client, id):
    """Retrieve the assistant with the given id"""
    sanitized_id = sanitize_id(id)
    my_assistant = client.beta.assistants.retrieve(sanitized_id)
    log_to_file("retrive_assistants", my_assistant)
    return my_assistant

def select_assistant(client,session):
    """Select an assistant from the list of assistants"""
    assistants = get_assistant_ids()
    assistant_opt_clompleter = WordCompleter(assistants)
    assistant_id = session.prompt(f"Please choose an assistant:\n",completer=assistant_opt_clompleter, complete_while_typing=True, style=Style.from_dict({'prompt': 'bold green'}))
    assistant = retrieve_assistant(client,assistant_id)
    print(f"Assistant name: {assistant.name}")
    
    return assistant

def update_assistant(client,id):
    pass

