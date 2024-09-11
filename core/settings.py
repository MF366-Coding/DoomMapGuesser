"""
# settings.py

**Handle the DoomMapGuesser settings.**
"""

import json

PATH = None


def register_path(given_path: str):
    global PATH
    PATH = given_path
    

def load_settings(**kw):
    with open(kw.get("path", PATH), 'r', encoding='utf-8') as f:
        return json.load(f)
    

def dump_settings(obj: dict, **kw):
    if 'overwrite' in kw:
        obj = kw['overwrite']
    
    with open(kw.get('path', PATH), 'w', encoding='utf-8') as f:
        json.dump(obj, f, indent=kw.get("indent", 4))
