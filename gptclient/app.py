import os

from openai import OpenAI


from textual import events, log, on
from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer
from textual.widgets import Button, Header, Footer, Input,Label,Select, Pretty, Static
from pathlib import Path
from gptclient.screens.chat_screen import ChatScreen
from gptclient.screens.assistants_screen import AssistantsScreen
from textual.binding import Binding

from gptclient.database import *


from gptclient.screens.chat_screen import get_api_key
   

class GptclientApp(App):
    
    CSS_PATH=Path(__file__).parent / "style/main_style.tcss"
    
    
    BINDINGS = [
        Binding("ctrl+q", action="quit", description="Quit"),
        Binding("ctrl+c", action="quit", description="Quit"),
        Binding("ctrl+a", action="create_assistant", description="Create assistant"),
        Binding("ctrl+c", action="set_chat", description="Chat tab"),]
    def __init__(self):
        
        super().__init__()
        self.dark = True
        self.assistant_id=None
        self.assistant_options = get_assistants_list() 
        self.usr_name = "User"
        #self.api_key = get_api_key()
        self.api_key = None
        self.client = None
        #log(locals())
    def compose(self) -> ComposeResult:
        
        """Create child widgets for the app."""
        yield Header()
        yield Label("GPT Client")
        yield Label("Enter your user name:")
        yield Input(id="usr_name",placeholder="User")
        yield Label("Select assistant:")
        yield Select(prompt="Select assistant:", options=self.assistant_options)
        yield Button("Create assistant", id="create_assistant")
        yield Button("Chat", id="set_chat")
        yield Footer()
        
    def on_mount(self) -> None:
        """Called when the app is mounted."""
        self.api_key = get_api_key()
        log()
        self.client = OpenAI(
            api_key=self.api_key
        )
        
        
    @on(Input.Changed, "usr_name")
    def usr_name_changed(self, event: Input.Changed) -> None:
        self.usr_name = str(event.value)
        
    @on(Select.Changed)
    def select_changed(self, event: Select.Changed) -> None:
        self.assistant_id = str(event.value) 
    
    @on(Button.Pressed, "#create_assistant")
    def action_create_assistant(self) -> None:
        self.push_screen(AssistantsScreen())
    
    @on(Button.Pressed, "#set_chat")    
    def action_set_chat(self) -> None:
        self.push_screen(ChatScreen())
        
        

            
            


app = GptclientApp()
    


if __name__ == '__main__':
    app.run()
    
