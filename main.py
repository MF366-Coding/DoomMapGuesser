import tkinter as tk
from tkinter.font import Font
from tkinter import ttk
import darkdetect
import pywinstyles
import random
import os
import sys
import simple_webbrowser
from PIL import ImageTk, Image
from core import level_db, scrapper, utils
from core.settings import SettingsObject
from core.database_handler import LOCAL, get_database
import math
import io
import requests
import json


ONLINE = 'online'

VERSION = 'v2.0.0'
LATEST = None

CONFIG_PATH: str = os.path.join(os.path.dirname(__file__), "settings.json")
ASSETS_PATH = os.path.join(os.path.dirname(__file__), 'assets')
ICONS_PATH = os.path.join(ASSETS_PATH, 'icons')
LOGO_PATH: str = os.path.join(ASSETS_PATH, "full_logo.png")
MAIN_ICON_PATH: str = os.path.join(ASSETS_PATH, "full_logo.ico")
THEME_PATH: str = os.path.join(ASSETS_PATH, 'sv.tcl')

settings = SettingsObject(CONFIG_PATH)


nl = utils.nullish_operator


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


def resize_image(image: Image.Image, wanted_width: int, width_is_height: bool = False, aspect_ratio: str = "detect", resample: int = Image.Resampling.LANCZOS, **kw) -> Image.Image:
    if width_is_height:
        new_width = None
        new_height = wanted_width
        
    else:
        new_width = wanted_width
        new_height = None
    
    match aspect_ratio:
        case '1:1':
            new_width = nl(new_width, wanted_width)
            new_height = nl(new_height, wanted_width)
        
        case "16:9":
            if new_width is None:
                new_width = int(new_height * (16 / 9))
                
            else:
                new_height = int(new_width * (9 / 16))
            
        case _:
            original_width, original_height = image.size
            
            if new_width is None:
                new_width = int(new_height * (original_width / original_height))
                
            else:
                new_height = int(new_width * (original_height / original_width))

    resized_logo = image.resize((new_width, new_height), resample, **kw)
    return resized_logo


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

DATABASES = settings.databases.copy()
DATABASES.insert(0, ["Default Database", "https://raw.githubusercontent.com/MF366-Coding/DoomMapGuesser/main/.github/ss_db.json", "NONE"])
CUR_DB = 0

HEADING1 = Font(root, family="SUSE ExtraBold", size=30)
HEADING2 = Font(root, family="SUSE Bold", size=22)
HEADING3 = Font(root, family='SUSE Semibold', size=17)
SUBTITLE = Font(root, family='SUSE Regular', size=12)
REGULAR_TEXT = Font(root, family='SUSE Regular', size=14)
LIGHT_TEXT = Font(root, family='SUSE Light', size=14)
BOLD_TEXT = Font(root, family='SUSE Medium', size=14)
GAME_TEXT = Font(root, family="Eternal UI", size=14)
GAME_BOLD = Font(root, family='Eternal UI', size=14, weight='bold')

PLAY_ITEMS = ttk.Frame(game_frame)


class __DialogErrorHappenedGeneralHidden(Exception): ...


def __SendDialogHiddenResponsive(*args):
    def __StopResponsiveAndHideMessage(*_):
        root.focus_force()
        
        try:
            __window.destroy()
            
        except __DialogErrorHappenedGeneralHidden:
            print(f'__StopResponsiveAndHideMessage failed to eliminate the message with id {id(__window)}')

    __window = tk.Toplevel(root)
    __window.focus_force()
    
    apply_theme_to_titlebar(__window, settings)
    
    __old_icon = Image.open(os.path.join(ICONS_PATH, "universal", f"{args[0].lower()}.png"))
    
    __icon_img = resize_image(
        image=__old_icon,
        wanted_width=100,
    )
    
    __window.__icon = ImageTk.PhotoImage(image=__icon_img)
    
    __window.title(args[1])
    __icon_widget = ttk.Label(__window, image=__window.__icon)
    __label = ttk.Label(__window, text=args[2], wraplength=args[3], font=args[4])
    
    __icon_widget.grid(column=0, row=0, padx=5, pady=5, ipadx=5, ipady=5)
    __label.grid(column=1, row=0, padx=5, pady=5, ipadx=5, ipady=5)
    
    __window.bind('<Button-1>', __StopResponsiveAndHideMessage)
    __window.bind('<Button-3>', __StopResponsiveAndHideMessage)


def send_dialog(dtype: str, title: str, message: str, wraplenght: int = 400, **kw):
    if dtype not in ('error', 'clock', 'warning', 'sucess', 'info'):
        return 
    
    __SendDialogHiddenResponsive(dtype, title, message, wraplenght, kw.get('overwrite_font', SUBTITLE))


def change_to_database(index: int):
    global CUR_DB
    
    CUR_DB = index
    
    if settings.offline_mode:
        if not DATABASES[index][2].startswith(('http://', 'https://', 'www.')):
            send_dialog('error', 'Invalid URL', "...") # TODO       


def generate_new_screenshot():
    raise NotImplementedError('TODO')


def setup_play_screen():
    PLAY_ITEMS.heading = ttk.Label(PLAY_ITEMS, text='Play', font=HEADING1)
    PLAY_ITEMS.f1 = ttk.Frame(PLAY_ITEMS)
    PLAY_ITEMS.f2 = ttk.Frame(PLAY_ITEMS)
    PLAY_ITEMS.f3 = ttk.Frame(PLAY_ITEMS)
    PLAY_ITEMS.f4 = ttk.Frame(PLAY_ITEMS)
    PLAY_ITEMS.f5 = ttk.Frame(PLAY_ITEMS.f4)
    PLAY_ITEMS.f6 = ttk.Frame(PLAY_ITEMS.f4)
    PLAY_ITEMS.f7 = ttk.Frame(PLAY_ITEMS.f4)
    PLAY_ITEMS.f8 = ttk.Frame(PLAY_ITEMS.f4)
    
    if settings.use_width_as_height:
        PLAY_ITEMS.f1.configure(height=settings.image_width + 20)
        
    else:
        PLAY_ITEMS.f1.configure(width=settings.image_width + 20)
        
    PLAY_ITEMS.cur_img = ImageTk.PhotoImage(
        resize_image(
            Image.open(os.path.join(ASSETS_PATH, 'error', 'image_none_yet.png')),
            settings.image_width,
            settings.use_width_as_height,
            settings.image_ratio
        )
    )
    
    PLAY_ITEMS.img_widget = ttk.Button(PLAY_ITEMS.f1, image=PLAY_ITEMS.cur_img, command=lambda:
        send_dialog('warning', 'TODO', 'Sadly, not done yet.')) # TODO
    
    PLAY_ITEMS.generation_butt = ttk.Button(PLAY_ITEMS.f2, text="Generate", command=lambda:
        send_dialog('warning', 'TODO', 'Sadly, not done yet.')) # TODO
    
    PLAY_ITEMS.guessing_butt = ttk.Button(PLAY_ITEMS.f2, text='Guess', command=lambda:
        send_dialog('warning', 'TODO', 'Sadly, not done yet.')) # TODO
    
    # TODO: after this it's just the game, episode, map and thingies


# [*] Sidebar Buttons
play_img = resize_image(
    Image.open(os.path.join(ICONS_PATH, settings.theme, 'play.png')),
    50,
    aspect_ratio='1:1'
)

play_tk = ImageTk.PhotoImage(play_img)

play_butt = ttk.Button(sidebar, image=play_tk, width=50, command=lambda:
    send_dialog('clock', 'Not Implemented Yet', str(random.choices(("Don't worry, we'll have DoomMapGuesser before GTA 6 xD", "Don't worry, DoomMapGuesser v2.0 is coming soon"), weights=(20, 80), k=1)[0])))

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
