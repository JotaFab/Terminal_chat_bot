import os

from time import sleep
from rich.prompt import Prompt
from rich.markdown import Markdown

from gptclient.database import *
from gptclient.methods import *


def get_assistant(client, console, assistant_id=None):
    
    if assistant_id is None:
        a = console.input("Do you want to create a new assistant? (y/n): \n")
        if a == "y":
            name = console.input("Enter the name for the assistant: \n")
            
            models = ["gpt-4-1106-preview", "gpt-3.5-turbo-1106"]
                
            model = Prompt.ask("Enter the model for the assistant  ", console=console, choices=models,default="gpt-3.5-turbo-1106")
            instructions = console.input("\nEnter the instructions for the assistant: \n")
            description = console.input("Enter the description for the assistant: \n")
            assistant = create_assistant(client,instructions, name, description,model)
            
            return assistant
        elif a == "n" :
            assistant_id = console.input("Enter the assistant id: \n")
            assistant = retrieve_assistant(client, assistant_id)
            return assistant
        else:
            console.print("Please enter a valid option: \n")
            get_assistant(client, console)
            
    else:
        try : assistant = retrieve_assistant(client, assistant_id)
        except Exception as e : console.print_exception(f"Assistant id is not valid: \n{e}")
    
def send_message(client,console, assistant, thread, prompt):
    
    #Create the message
    message = create_message(client, thread.id, prompt)
    #Create the run
    run = create_run(client, thread.id, assistant.id)
    #Retrieve the run and check if it is completed
    sleep(1)
    run_retrieve = retrieve_run(client, thread_id=thread.id, run_id=run.id)
    steps_list = list_run_steps(client,thread.id,run.id)
    console.print(steps_list.data[0].status)
    while steps_list.data[0].status != "completed":
        sleep(1)  # Wait for 1 second before checking the status again
        steps_list = list_run_steps(client,thread.id,run.id)
    
    
    message_retrived= retrieve_message(client,thread_id=thread.id,message_id=steps_list.data[0].step_details.message_creation.message_id)
    
    
    return message_retrived
    

def chat(client, console):
    """quiero crear una interfaz en la de un chat en el que pueda conversar """
    
    
    """Comprobar de una sesion previa el assistant_id si no se encuentra create_assistant, con el assistant_id retrive the assistant, Create a thread , in a loop create a message, create a run, a run step, and print the response"""
    
    chat_config = get_chat_config()
    if not get_chat_config():    
        assistant = get_assistant(client, console)
        usr_name = console.input("Enter your name: \n")
        thread = None
        try:
            thread = create_thread(client)
        except Exception:
            console.print_exception()
        insert_chat_config(assistant.id,thread.id,usr_name)
        chat_config = get_chat_config()
    assistant = retrieve_assistant(client, chat_config['assistant_id'])
    #console.print(assistant.name)
    thread = create_thread(client)
    #console.print(thread)
    usr_name = chat_config['usr_name']
    
    print(f"Welcome to the chat {usr_name}!")
    
    message = console.input(f"{usr_name}: \n")
    while message.lower() != "quit":
        try:
            message_content=send_message(client,console, assistant, thread, message)
            
            console.print(f"{assistant.name}: \n")
            print_message(console, message_content)
        except:
            console.print_exception()
        
        message = console.input(f"{usr_name}: \n")
            
        
    console.print("Bye!")        
        
def print_message(console, message):
    md = Markdown(message.value)
    console.print(md)
    
    for annotation in message.annotations:
        console.print(f"{annotation}")