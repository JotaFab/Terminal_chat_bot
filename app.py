import os
import json
import random
import sys
from rich.console import Console
from rich.markdown import Markdown
from openai import OpenAI
import time

def create_assistant(client):
    
    assistant = client.beta.assistants.create(
        model="gpt-3.5-turbo-16k-0613",
        name="Shell-Gpt",
        description="You are a code terminal assistant. You have to have knowledge of bash python and any other shell specifically for instructions in debian.",
        instructions=" Give me alternatives in code for shell or python if i need it. You will first give the code and then after all the code an explanation and all the code need to have comments of how it works",
        tools=[{"type": "code_interpreter"}],
        
    )
    return assistant

def retrive_assistant(client,id):
    my_assistant = client.beta.assistants.retrieve(id)
    return my_assistant

def create_thread(client):
    thread = client.beta.threads.create()
    return thread


def send_message(client,assistant, thread, prompt):

    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=prompt
    )
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
        instructions="Please address the user as JotaFab"
    )
    time.sleep(1)
    run_steps = client.beta.threads.runs.steps.list(
        thread_id=thread.id,
        run_id=run.id
    )
    
    
    while run_steps.data[0].status != "completed":
        time.sleep(1)  # Wait for 1 second before checking the status again
        run_steps = client.beta.threads.runs.steps.list(thread_id=thread.id, run_id=run.id)
        
    
    message = client.beta.threads.messages.retrieve(
        thread_id=thread.id,
        message_id=run_steps.data[0].step_details.message_creation.message_id
    ) 
       
    return message

"""def get_message(client, assistant, thread, message):
    response = client.beta.threads.messages.retrieve(
        thread_id=thread.id,
        message_id=message.id
        
    )
    return response"""

            
def main():
    if len(sys.argv) > 1:
        # Obtener el primer argumento
        prompt = sys.argv[1]
    else:
        print("No se pasaron argumentos.")
        return
    
    console = Console()
    key = os.environ.get("OPENAI_API_KEY")

 
    client = OpenAI(
        api_key=key,
        organization='org-HisdlnrnC90sbXwyPfQqWu9k'
        
    )
    
    assistant= retrive_assistant(client,id="asst_oIDpBKU6zFBY5TbkvfaVuIav")
    usr_thread =create_thread(client)
    msg = send_message(client,assistant , usr_thread, prompt)
    response = msg.content[0].text.value
    md = Markdown(response)
    console.print(md)
    
    
if __name__=="__main__":
    main()
    # 
    
