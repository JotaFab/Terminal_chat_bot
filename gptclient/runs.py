

def create_run(client,thread,assistant):
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
        instructions="Please address the user as JotaFab"
    )
    return run

def retrieve_run(client,thread,run):
    run_retrieve = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id,
    )
    return run_retrieve

def list_runs(client,thread):
    list_runs= client.beta.threads.runs.list(
        thread_id=thread.id,
    )
    return list_runs

def list_steps(client,thread,run):
    list_steps=client.beta.threads.runs.steps.list(
        thread_id=thread.id,
        run_id=run.id,
    )
    return list_steps
    

def run_steps(client,thread,run,step):
    run_steps=client.beta.threads.runs.steps.retrieve(
        thread_id=thread.id,
        run_id= run.id,
        step_id=step.id,
    )
    return run_steps


