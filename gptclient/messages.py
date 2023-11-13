from runs import create_run, retrieve_run, list_steps
import time
from gptclient.logs import log_to_file

def create_message(client,thread,prompt):
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=prompt,
    )
    log_to_file("messages", message)
    return message

def retrieve_message(client,thread,msg_id):
    message= client.beta.threads.messages.retrieve(
        thread_id=thread.id,
        message_id=msg_id,
    )
    return message.content[0].text.value

def modify_mssage(client,thread,msg_id,metadata_json):
    message = client.beta.threads.messages.retrieve(
        message_id=msg_id,
        thread_id=thread.id,
        metadata=metadata_json,
    )
    return message

def list_messages(client,thread):
    thread_messages=client.beta.threads.messages.list(
        thread_id=thread.id
    )
    return thread_messages


def send_message(client, assistant, thread, prompt):
    message = create_message(client, thread, prompt)
    run = create_run(client, thread, assistant)
    run_retrieve = retrieve_run(client, thread, run)
    time.sleep(1)
    steps_list = list_steps(client,thread,run)
    
    while steps_list.data[0].status != "completed":
        time.sleep(1)  # Wait for 1 second before checking the status again
        steps_list = list_steps(client,thread,run)
    
    message_retrived= retrieve_message(client,thread,steps_list.data[0].step_details.message_creation.message_id)
    
    return message_retrived