from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Button, Header, Footer, Select, Input,Label,Pretty, Static
from textual import events, on, log 
from gptclient.methods import create_assistant
from gptclient.database import insert_assistant

model_options = [("gpt-4-1106-preview","gpt-4-1106-preview"),("gpt-3.5-turbo-1106","gpt-3.5-turbo-1106")]

class AssistantsScreen(Screen):
    
    def __init__(self):
        super().__init__()
        
    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Label("Assistant options:")
        yield Label("Name")
        yield Input(id="usr_name",placeholder="Jota")
        yield Label("Instructions")
        yield Input(id="instructions",placeholder="You are an assistant for software development topics.")
        yield Label("GPT model")
        yield Select(prompt="Select GPT model:", options=model_options)
        #yield Label("Files:")
        #yield Button("Upload files")
        yield Button("Create Assistant", id="create_assistant")
        yield Footer()
        
    def on_mount(self, event) -> None:
        self.assistant_name = None
        self.instructions = None
        self.model = None

    @on(Select.Changed)
    def select_changed(self, event: Select.Changed) -> None:
        self.model = str(event.value)
        
    @on(Input.Changed, "#usr_name")
    def usr_name_changed(self, event: Input.Changed) -> None:
        self.assistant_name = str(event.value)
        
    @on(Input.Changed, "#instructions")
    def instructions_changed(self, event: Input.Changed) -> None:
        self.instructions = str(event.value)
        
    @on(Button.Pressed, "#create_assistant")
    def create_assistant(self) -> None:
        Button(id="create_assistant", label="Creating assistant", disabled=True,variant="warning")
        log("Creating assistant")
        log(self.app.client)
        log(self.assistant_name)
        log(self.instructions)
        log(self.model)
        
        assistant = create_assistant(client=self.app.client,instructions=self.instructions, name=self.assistant_name, model=self.model)
        insert_assistant(assistant)
        log(assistant)
        
        Button(id="create_assistant", label="Assistant created", disabled=False, variant="success")