
from openai import OpenAI

def create_assistant(client,assis_name):
    
    assistant = client.beta.assistants.create(
        model="gpt-3.5-turbo-16k-0613",
        name=assis_name,
        description="You are a code terminal assistant. You have to have knowledge of bash python and any other shell specifically for instructions in debian.",
        instructions=" Give me alternatives in code for shell or python if i need it. You will first give the code and then after all the code an explanation and all the code need to have comments of how it works",
        tools=[{"type": "code_interpreter"}],
        
    )
    return assistant

def retrive_assistant(client,id):
    my_assistant = client.beta.assistants.retrieve(id)
    return my_assistant