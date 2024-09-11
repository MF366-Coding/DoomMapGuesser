import tkinter as tk
from tkinter import ttk
import random
import os
import sys
import simple_webbrowser
from PIL import ImageTk, Image
from core import level_db, scrapper
from core.settings import SettingsObject
import math
import io
import requests
import json
import importlib
from argparse import ArgumentParser
from tkinter.font import Font

VERSION = 'v2.0.0'
LATEST = None

CONFIG_PATH: str = os.path.join(os.path.dirname(__file__), "settings")
LOGO_PATH: str = os.path.join(os.path.dirname(__file__), "assets", "full_logo.png")
ICON_PATH: str = os.path.join(os.path.dirname(__file__), "assets", "full_logo.ico")
FONT_PATH: str = os.path.join(os.path.dirname(__file__), 'assets', 'font.ttf')
THEME_PATH: str = os.path.join(os.path.dirname(__file__), 'assets', 'sv.tcl')

settings = SettingsObject(CONFIG_PATH)

root = tk.Tk()
root.title(f'DoomMapGuesser by MF366 - {VERSION}')
if sys.platform == 'win32':
    root.iconbitmap(ICON_PATH)

sidebar = ttk.Frame(root, width=80)

# TODO

# [!?] https://github.com/rdbende/Sun-Valley-ttk-theme (Sun Valley theme)
root.tk.call("source", os.path.join(THEME_PATH))
style = ttk.Style(root)
style.theme_use("sun-valley-dark")

