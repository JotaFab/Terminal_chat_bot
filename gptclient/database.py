from tinydb import TinyDB, Query
import os
import datetime
from pathlib import Path
"""create a tinydb database"""



chat_config_history_path = Path(__file__).parent/"chat_config.json"
if not os.path.exists(chat_config_history_path):
    open(chat_config_history_path, 'a').close()
    

db = TinyDB(chat_config_history_path)
User = Query()

"""create a table in the database"""
def insert_assistant(assistant):
    """insert the assistant in the database and timestamp it"""
    assistant_table = db.table('assistants')
    _id = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    assistant_table.insert({'id': _id,'assistant_id': assistant.id, 'name': assistant.name, 'model': assistant.model, 'instructions': assistant.instructions})
    
def get_assistants_list():
    """get the list of assistants names from the database"""
    assistant_table = db.table('assistants')
    assistants = assistant_table.all()
    assistants_names = [(assistant["name"], assistant["assistant_id"]) for assistant in assistants]
    return assistants_names


def insert_chat_config(assistant_id, thread_id, usr_name):
    """insert the chat config in the database and timestamp it"""
    chat_config_table = db.table('chat_config')
    _id = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    chat_config_table.insert({'id': _id,'assistant_id': assistant_id, 'thread_id': thread_id, 'usr_name': usr_name})


    
def get_chat_config():
    """get the chat config from the last session from the database comprueba primero si existe el archivo de la base de datos sino devuelve false"""
    if os.path.exists(chat_config_history_path):
        try:
            chat_config = db.table('chat_config').all()[-1]
            return chat_config
        except Exception:
            return False
    else:
        return False