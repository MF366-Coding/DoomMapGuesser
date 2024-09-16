import tkinter as tk
from tkinter import ttk
import darkdetect
import pywinstyles
import random
import os
import sys
import simple_webbrowser
from tkinter import messagebox as mb
from PIL import ImageTk, Image
from core import level_db, scrapper
from core.settings import SettingsObject
from core.database_handler import LOCAL, get_database
import math
import io
import requests
import json
import importlib
from argparse import ArgumentParser
from tkinter.font import Font

ONLINE = 'online'

VERSION = 'v2.0.0'
LATEST = None

CONFIG_PATH: str = os.path.join(os.path.dirname(__file__), "settings.json")
ASSETS_PATH = os.path.join(os.path.dirname(__file__), 'assets')
ICONS_PATH = os.path.join(ASSETS_PATH, 'icons')
LOGO_PATH: str = os.path.join(ASSETS_PATH, "full_logo.png")
MAIN_ICON_PATH: str = os.path.join(ASSETS_PATH, "full_logo.ico")
FONT_PATH: str = os.path.join(ASSETS_PATH, 'font.ttf')
THEME_PATH: str = os.path.join(ASSETS_PATH, 'sv.tcl')

settings = SettingsObject(CONFIG_PATH)


def autodetect_theme(configs: SettingsObject):    
    if configs.theme == 'auto':
        if sys.platform != 'win32':
            configs.theme = 2 # [i] default to dark if not available
        
        else:
            new_theme = darkdetect.theme()
            
            if new_theme is None:
                configs.theme = 2
            
            else:
                configs.theme = new_theme.lower()
                print(f'autodetected to: {new_theme}')
            
    configs.save_settings()


def apply_theme_to_titlebar(window: tk.Tk, configs: SettingsObject):
    if sys.platform != 'win32':
        return # [i] completely ignore this
    
    version = sys.getwindowsversion()

    if configs.theme == 'auto':
        autodetect_theme(configs)
    
    if version.major == 10 and version.build >= 22000:
        pywinstyles.change_header_color(window, "#1c1c1c" if configs.theme == "dark" else "#fafafa")
        
    elif version.major == 10:
        pywinstyles.apply_style(window, "dark" if configs.theme == "dark" else "normal")

        # [i] force Windows 10 to update because it doesn't (stupid Microsoft :upside_down:)
        window.wm_attributes("-alpha", 0.99)
        window.wm_attributes("-alpha", 1)

    configs.save_settings()


root = tk.Tk()
root.title(f'DoomMapGuesser by MF366 - {VERSION}')
root.geometry('900x700')

if sys.platform == 'win32':
    root.iconbitmap(MAIN_ICON_PATH)

autodetect_theme(settings)
apply_theme_to_titlebar(root, settings)

sidebar = ttk.Frame(root, width=80)
main_frame = ttk.Frame(root, width=820)

database_bar = ttk.Frame(main_frame, height=80)
game_frame = ttk.Frame(main_frame)


# [*] Sidebar Buttons
play_img = Image.open(os.path.join(ICONS_PATH, settings.theme, 'play.png'))
resized_play_img = play_img.resize((50, 50), Image.Resampling.LANCZOS)

del play_img

play_tk = ImageTk.PhotoImage(resized_play_img)

play_butt = ttk.Button(sidebar, image=play_tk, width=50, command=lambda:
    mb.showerror('n/i', "not implemented"))

play_butt.pack()

database_bar.pack()
game_frame.pack()

sidebar.grid(column=0, row=0)
main_frame.grid(column=1, row=0)

# TODO

# [!?] https://github.com/rdbende/Sun-Valley-ttk-theme (Sun Valley theme)
root.tk.call("source", os.path.join(THEME_PATH))
style = ttk.Style(root)
style.theme_use(f"sun-valley-{settings.theme}")

root.mainloop()
