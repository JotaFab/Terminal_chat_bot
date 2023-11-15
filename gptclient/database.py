from tinydb import TinyDB, Query
import os
import datetime
"""create a tinydb database"""

usr_path=os.path.expanduser('~')
chat_config_history_path = f'{usr_path}/.chat_config.json'
if not os.path.exists(chat_config_history_path):
    open(chat_config_history_path, 'w').close()
    

db = TinyDB(chat_config_history_path)
User = Query()

"""create a table in the database"""

def insert_chat_config(assistant_id, thread_id, usr_name):
    """insert the chat config in the database and timestamp it"""
    _id = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    db.insert({'id': _id,'assistant_id': assistant_id, 'thread_id': thread_id, 'usr_name': usr_name})


    
def get_chat_config():
    """get the chat config from the last session from the database comprueba primero si existe el archivo de la base de datos sino devuelve false"""
    if os.path.exists(chat_config_history_path):
        try:
            chat_config = db.all()[-1]
            return chat_config
        except Exception:
            return False
    else:
        return False