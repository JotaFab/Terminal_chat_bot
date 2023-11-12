import os
import sys
from rich.console import Console
from rich.markdown import Markdown
from openai import OpenAI
import click
from prompt_toolkit import prompt
from prompt_toolkit.styles import Style
from prompt_toolkit import print_formatted_text as print

from assistant import create_assistant, retrive_assistant
from messages import send_message
from threads import create_thread




#@click.option(prompt='Your prompt', help='Ask something')
@click.command()
@click.option('--api_key', '-k', help='Openai API key. If not provided, will prompt for it or use the environment variable OPENAI_API_KEY.')
def main(api_key):
    
    

    console = Console()
    key = os.environ.get("OPENAI_API_KEY") or api_key

    client = OpenAI(
        api_key=key,
        organization='org-HisdlnrnC90sbXwyPfQqWu9k'  
    )
    if key:
        try:
            client.models.list()
            
        except KeyboardInterrupt:
            click.echo("KeyboarInterrupt... \n Exiting...")
            exit(0)
    
    usr_name = prompt("Enter your username: \n")
    
    try:
        usr_prompt = prompt(f"{usr_name}: \n")
        while usr_prompt.lower() != "q" or "quit" or "exit":
            assistant = retrive_assistant(client,id="asst_oIDpBKU6zFBY5TbkvfaVuIav")
            usr_thread =create_thread(client)
            msg = send_message(client,assistant , usr_thread, usr_prompt)
            #md_others = others
            md = Markdown(msg)
            print(f"{assistant.name}: \n")
            console.print(md)
            
            #console.print(others)
            usr_prompt = prompt(f"{usr_name}: \n")
    except Exception as e:
        print(f"Error: {e}", 'light_red')
        exit(1)
    except KeyboardInterrupt:
        print(f"Keyboard Interrupt, Exiting...", 'light_red')
        exit(0)
    
if __name__=="__main__":
    main()
    # 