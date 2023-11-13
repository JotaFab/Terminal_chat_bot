import json
import os
from gptclient.logs import log_to_file

path = os.getcwd()

def create_thread(client, session):
    """Create a new thread and save it to a log file, print the log in app_log.txt, and return the thread"""
    thread = client.beta.threads.create()
    log_to_file("threads", thread)
    with open(f"{path}/logs/thread_ids.txt", "a") as f:
        f.write(f"{thread.id}\n")
    return thread
def get_last_thread_id():
    with open(f"{path}/logs/thread_ids.txt", "r") as f:
        thread_id = f.readlines()[-1]
    f.close()
    sanitize_id(thread_id)
    return thread_id
        
    
def get_thread_ids():
    
    with open(f"{path}/logs/thread_ids.txt", "r") as f:
        thread_id = f.readlines()
        thread_id = [x.strip() for x in thread_id]
        thread_id.reverse()
    return thread_id

def sanitize_id(id):
    
    return ''.join(c for c in id if c.isprintable())

def select_thread(client, session):
    """Select a thread from the log file, print the log in app_log.txt, and return the thread"""
    
    thread_id = session.prompt("Enter the thread id: \n")
    sanitize_id(thread_id)
    select_thread = client.beta.threads.retrieve(thread_id=thread_id)
    log_to_file("select_threads", select_thread)
    return select_thread

def retrieve_thread(client, session, thread_id=None):
    """Retrieve a thread from the log file, print the log in app_log.txt, and return the thread"""
    if thread_id == None:
        try: thread_id = get_last_thread_id()
        except: thread_id = session.prompt("Enter the thread id: \n")
        
        
    retrive_thread = client.beta.threads.retrieve(thread_id=thread_id)
    log_to_file("retrive_threads", retrive_thread)
    return retrive_thread
