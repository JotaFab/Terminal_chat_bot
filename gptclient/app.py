import os
from rich.console import Console
from rich.markdown import Markdown
from openai import OpenAI
import click
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit import PromptSession
from prompt_toolkit import print_formatted_text as print
from gptclient.options import chose_options
from prompt_toolkit.styles import Style
from gptclient.options import assistant_options,chat,thread_options,file_options
from prompt_toolkit import Application
def get_openai_client(api_key):
    key = os.environ.get("OPENAI_API_KEY") or api_key
    client = OpenAI(
        api_key=key,
        organization='org-HisdlnrnC90sbXwyPfQqWu9k'
    )
    return client


banner = """
_________  ___  ___  _________  ________  ________  ________  ________  ________  ___  ___  ___  ________  ___  ___  ___  ________  ________  ________  ________  _______      
|\___   ___\\  \|\  \|\___   ___\\   __  \|\   __  \|\   __  \|\   __  \|\   __  \|\  \|\  \|\  \|\   ____\|\  \|\  \|\  \|\   __  \|\   __  \|\   ____\|\   __  \|\  ___ \     
\|___ \  \_\ \  \\\  \|___ \  \_\ \  \|\  \ \  \|\  \ \  \|\  \ \  \|\  \ \  \|\  \ \  \\\  \ \  \ \  \___|\ \  \\\  \ \  \\\  \ \  \|\  \ \  \|\  \ \  \___|\ \  \|\  \ \   __/|    
     \ \  \ \ \   __  \   \ \  \ \ \   _  _\ \   __  \ \   _  _\ \   __  \ \   __  \ \   __  \ \  \ \  \    \ \   __  \ \  \\\  \ \   _  _\ \   __  \ \  \    \ \   _  _\ \  \_|/__  
      \ \  \ \ \  \ \  \   \ \  \ \ \  \\  \\ \  \ \  \ \  \\  \\ \  \ \  \ \  \ \  \ \  \ \  \ \  \ \  \____\ \  \ \  \ \  \\\  \ \  \\  \\ \  \ \  \ \  \____\ \  \\  \\ \  \_|\ \ 
       \ \__\ \ \__\ \__\   \ \__\ \ \__\\ _\\ \__\ \__\ \__\\ _\\ \__\ \__\ \__\ \__\ \__\ \__\ \__\ \____ 
"""


@click.command()
@click.option('--api_key', '-k', help='Openai API key. If not provided, will prompt for it or use the environment variable OPENAI_API_KEY.')
def main(api_key):
    
    session = PromptSession()
    
    print(f"Welcome to the GPT Terminal Assistant!\n\n")
    print(f"To do: \n\n {banner} \n\n")
    try:
        client = get_openai_client(api_key)
    except Exception as e:
        print(f"Error: {e}", 'light_red')
        exit(1)
    try:
        client = get_openai_client(api_key)
        
        chose_options(client,session)
    except Exception as e:
        print(f"Error: {e}", 'light_red')
        exit(1)
    
        
if __name__=="__main__":
    
    main()      