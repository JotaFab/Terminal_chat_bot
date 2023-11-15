# Description: This file contains all the methods used in the gptclient package
default_options = {
    "instructions": "You are an assistant for software development topics.",
    "name": "Gptclient",
    "model": "gpt-3.5-turbo-1106",
    "description": "This assistant can help you with various software development tasks.",
}

#Assistant methods

def create_assistant(client,instructions=None, name=None, description=None, model=None):
    
    """Create an assistant with the given parameters, return the created assistant"""
    
    if instructions is None:
        instructions = default_options["instructions"]
    else:
        instructions = default_options["instructions"] + " " + instructions
    if description is None:
        description = default_options["description"]
    else:
        description = default_options["description"] + " " + description
    if name is None:
        name = default_options["name"]
        
    if model is None:
        model = default_options["model"]
        
    my_assistant = client.beta.assistants.create(
        instructions=instructions,
        name=name,
        tools=[{"type": "code_interpreter"}],
        model=model,
        description=description,
    )
    return my_assistant

def retrieve_assistant(client, assistant_id):
    """Retrieve the assistant with the given id"""
    assistant=client.beta.assistants.retrieve(assistant_id)
    return assistant

def modify_assistant(client, assistant_id, additional_instructions="", additional_description="", name=default_options["name"], model=default_options["model"]):
    """Modify the assistant with the given id, return the modified assistant"""
    instructions = default_options["instructions"] + " " + additional_instructions
    description = default_options["description"] + " " + additional_description
    my_updated_assistant = client.beta.assistants.update(
        id=assistant_id,
        instructions=instructions,
        name=name,
        tools=[{"type": "code_interpreter"}],
        model=model,
        description=description,
       )   
    return my_updated_assistant

def delete_assistant(client, assistant_id):
    """Delete the assistant with the given id, return deletion status"""
    response = client.beta.assistants.delete(assistant_id)
    return response

def list_assistants(client):
    """List all assistants, return the list of assistants"""
    assistants = my_assistants = client.beta.assistants.list(
        order="desc",
        limit="20",
    )   
    return assistants

#Thread methods

def create_thread(client):
    empty_thread = client.beta.threads.create()
    return empty_thread

def retrieve_thread(client, thread_id):
    thread = client.beta.threads.retrieve(thread_id)
    return thread

def delete_thread(client, thread_id):
    response = client.beta.threads.delete(thread_id)
    return response

#message methods

def create_message(client, thread_id,message,file_ids=[]):
    thread_message = client.beta.threads.messages.create(thread_id,role="user", content=message, file_ids=file_ids)
    return thread_message

def retrieve_message(client, message_id, thread_id ):
    message = client.beta.threads.messages.retrieve(
        message_id=message_id, 
        thread_id=thread_id
    )
    
    # Extract the message content
    message_content = message.content[0].text
    annotations = message_content.annotations
    citations = []

    # Iterate over the annotations and add footnotes
    for index, annotation in enumerate(annotations):
        # Replace the text with a footnote
        message_content.value = message_content.value.replace(annotation.text, f' [{index}]')

        # Gather citations based on annotation attributes
        if (file_citation := getattr(annotation, 'file_citation', None)):
            cited_file = client.files.retrieve(file_citation.file_id)
            citations.append(f'[{index}] {file_citation.quote} from {cited_file.filename}')
        elif (file_path := getattr(annotation, 'file_path', None)):
            cited_file = client.files.retrieve(file_path.file_id)
            citations.append(f'[{index}] Click <here> to download {cited_file.filename}')
            # Note: File download functionality not implemented above for brevity

    # Add footnotes to the end of the message before displaying to user
    
    message_content.value += '\n' + '\n'.join(citations)
    return message_content
    
def list_messages(client, thread_id):
    messages = client.beta.threads.messages.list(thread_id)
    return messages

#run methods

def create_run(client, thread_id, assistant_id):
    run = client.beta.threads.runs.create(
        thread_id=thread_id, 
        assistant_id=assistant_id
    )
    return run

def retrieve_run(client, thread_id, run_id):
    run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
    return run

def list_runs(client, thread_id):
    runs = client.beta.threads.runs.list(thread_id)
    return runs

#run steps methods

def retrieve_run_step(client, thread_id,run_id,step_id):
    run_step = client.beta.threads.runs.steps.retrieve(
        thread_id=thread_id,
        run_id=run_id,
        step_id=step_id
    )
    return run_step

def list_run_steps(client, thread_id,run_id):
    run_steps = client.beta.threads.runs.steps.list(
        thread_id=thread_id,
        run_id=run_id
    )
    return run_steps

