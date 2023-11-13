from rich.console import Console
from rich.markdown import Markdown
#from openai import OpenAI
from prompt_toolkit.completion import WordCompleter
#from prompt_toolkit import prompt
from prompt_toolkit import print_formatted_text as print

from gptclient.messages import send_message
from gptclient.threads import create_thread, retrieve_thread
from gptclient.assistant import retrieve_assistant, create_assistant, select_assistant,update_assistant
import json
from prompt_toolkit.styles import Style



def get_user_name(session):
    usr_name = session.prompt("Enter your username: \n")
    return usr_name

def get_user_prompt(usr_name,session):
    usr_prompt = session.prompt(f"{usr_name}: \n")
    return usr_prompt

def print_assistant_message(assistant, message,session):
    console = Console()
    md = Markdown(message)
    console.log(f"{assistant.name}: \n", style="white on blue")
    console.print(md)


    
    

def chat(client,session):
    usr_name = get_user_name(session)
    assistant = None
    assistant_id = None
    try: assistant = select_assistant(client,session)
    except: assistant = create_assistant(client,session)
    assistant_id = assistant.id
    try:
        thread_id = None    
        
        try: thread_id = retrieve_thread(client,session)
        except: thread_id = create_thread(client,session)  
              
        thread = retrieve_thread(client,session, thread_id)
        usr_prompt = get_user_prompt(usr_name,session)
        
        while usr_prompt.lower() not in ["q", "quit", "exit"]:
            usr_thread = retrieve_thread(client, thread)
            msg = send_message(client, assistant, usr_thread, usr_prompt)
            print_assistant_message(assistant, msg,session)
            usr_prompt = get_user_prompt(usr_name,session)

    except Exception as e:
        print(f"Error: {e}", 'light_red')
        exit(1)
    except KeyboardInterrupt:
        print(f"Keyboard Interrupt, Exiting...", 'light_red')
        chat(client)


def assistant_options(client,session):
    assistant_options = {
        "create_assistant": create_assistant,
        "retrive_assistant": select_assistant,
        "update_assistant": update_assistant, 
    }
    assistant_opt_completer = WordCompleter(assistant_options.keys())
    chose_options(client,session, assistant_options, assistant_opt_completer)
    
    
    

def thread_options(client,session):
    thread_options = {
        "create_thread": create_thread,
        "retrive_thread": retrieve_thread,
    }
    thread_opt_completer = WordCompleter(thread_options.keys())
    chose_options(client,session, thread_options, thread_opt_completer)
    

def file_options(client,session):
    print("File options: \n")
    # Your code here



def chose_options(client, session, options=None, opt_clompleter=None):
    if options is None:
        options = {
        "assistant_options": assistant_options,
        "chat": chat,
        "thread_options": thread_options,
        "file_options": file_options,
        "exit": exit,
    }
    if opt_clompleter is None:
        opt_clompleter = WordCompleter(options.keys())    
    
    # print(f"{options.keys()} \n")
    try:
        chosen_option = session.prompt("Choose an option: \n", completer=opt_clompleter, complete_while_typing=True, style=Style.from_dict({'prompt': 'bold blue'}))
        while chosen_option in options:
            if chosen_option == "exit":
                exit()
            options[chosen_option](client,session)
            chosen_option = session.prompt("Choose an option: \n", completer=opt_clompleter, complete_while_typing=True, style=Style.from_dict({'prompt': 'bold blue'}))
        
    except KeyboardInterrupt:
        print(f"Keyboard Interrupt, returning to main...", 'light_red')
        chose_options(client,session)
    
    
    except Exception as e:
        print(f"Error: {e}", 'light_red')
        exit(1)
    