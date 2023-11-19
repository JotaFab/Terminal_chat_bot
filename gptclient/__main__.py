import click

from gptclient.app import GptclientApp


@click.group(invoke_without_command=True)
@click.pass_context
def main(context: click.Context) -> None:
    """
    Gptclient: A personalizable GPT-Asisstant
    """
    
    app = GptclientApp()
    
    if context.invoked_subcommand is None:
        
        app.run()
        
        
@main.command()
def reset():
    """Reset the database"""
    #TODO
    pass

@main.command()
@click.argument("file", type=click.File("r"))
def import_file(file : click.File):
    """Import data from a file"""
    #TODO
    pass

@main.command()
def chat():
   """Start a chat with the assistant"""
   #TODO
   pass


if __name__ == "__main__":
    main()

