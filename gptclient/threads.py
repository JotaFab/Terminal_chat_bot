

def create_thread(client):
    thread = client.beta.threads.create()
    return thread

def retrive_thread(client,thread):
    retrive_thread = client.beta.threads.retrieve(
        thread_id=thread.id
    )
    return retrive_thread

