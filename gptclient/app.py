import os
import readline
import rlcompleter
from openai import OpenAI
from rich.console import Console
from rich.traceback import install
from rich.prompt import Prompt
from gptclient.chat import chat

install(show_locals=True)
console = Console(stderr=True)

def valid_api_key(api_key):
    """Check if the api_key is valid"""
    client = OpenAI(api_key=api_key)
    try:
        client.models.list()
        return True
    except Exception as e:
        console.print_exception(f"Error: {e}")
        return False
    
    
    
def get_api_key():
    """Get the OpenAI API key from the environment variable OPENAI_API_KEY if it exists, otherwise prompt the user for it."""
    api_key = None
    if os.environ.get("OPENAI_API_KEY"):
        api_key = os.environ["OPENAI_API_KEY"]
        if not valid_api_key(api_key):
            api_key = None
        else:
            console.print(f"Using API key from environment variable OPENAI_API_KEY", style="bold green")
    else:
        api_key = console.input("Enter your OpenAI API key: \n")
        while not api_key.startswith("sk-"):
            if not valid_api_key(api_key):
                api_key = None
                api_key = console.input("Enter a valid OpenAI API key: \n", style="bold red")
        return api_key
                
        
        """comprobar que la key tenga un formato valido"""
    
    return api_key
    
def main():
    """Main function"""
    # Validar la api_key
    api_key = get_api_key()
    
    # Crear el cliente de OPENAI
    client = OpenAI(api_key=api_key)
    
    
    # Iniciar el chat
    try:
        chat(client, console)
    except Exception as e:
        console.print_exception( f"Error: {e}")
        exit(1)
        
    return

if __name__ == '__main__':
    main()
    