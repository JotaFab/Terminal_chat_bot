import click

def select_assistant():
    assistants = ['assistant1', 'assistant2', 'assistant3']
    assistant = click.prompt('Please choose an assistant', type=click.Choice(assistants))
    return assistant

select_assistant()