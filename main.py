import tkinter as tk
import random
import os
import sys
import json
import simple_webbrowser
from PIL import ImageTk
from core import level_db, scrapper

LOGO_PATH = os.path.join(os.path.dirname(__file__), "assets", "full_logo.png")
ICON_PATH = os.path.join(os.path.dirname(__file__), "assets", "full_logo.ico")

root = tk.Tk()
root.title("Doom Map Guesser by MF366 - The GeoGuesser of DOOM")
root.resizable(True, False)

if sys.platform == 'win32':
    root.iconbitmap(ICON_PATH)

f1 = tk.Frame(root)
f2 = tk.Frame(root)
f3 = tk.Frame(f2)
f4 = tk.Frame(f2)
f5 = tk.Frame(root)

database: dict[str, dict[str, dict[str, list[int]]]] = {
    "Doom (1993) / The Ultimate Doom": level_db.ultimate_doom,
    "Doom II": level_db.doom_ii,
    "Doom II: Master Levels": level_db.doom_ii_master_levels,
    "Final Doom: TNT Evilution": level_db.final_doom_tnt_evilution,
    "Final Doom: The Plutonia Experiment": level_db.final_doom_plutonia_experiment,
    "Doom 64": level_db.doom_64,
    "No Rest for the Living": level_db.no_rest_for_the_living
}

screenshot_database: dict[str, list[str]] = scrapper.scrape_json_contents("https://raw.githubusercontent.com/MF366-Coding/DoomMapGuesser/main/.github/ss_db.json")


def pick_new_game_wad():
    new_game_wad: str = random.choice(list(database.keys()))
    return new_game_wad


def pick_new_episode(game: str):
    new_episode = random.choice(list(database[game].keys()))
    return new_episode


def pick_new_map(game: str, episode: str) -> tuple[str, int, int]:
    new_map = random.choice(list(database[game][episode].keys()))
    return new_map, database[game][episode][new_map][0], database[game][episode][new_map][1]


def pick_new_screenshot(map_id: int, current_screenshot_link: str, attempts: int = 10) -> str | bool:
    new_screenshot = current_screenshot_link
    map_id = str(map_id)
    
    for _ in range(attempts):
        if map_id not in screenshot_database.keys():
            return False # [i] no screenshots for given map
        
        new_screenshot: str = random.choice(screenshot_database[map_id])
        
        if new_screenshot == current_screenshot_link:
            continue # [i] same screenshot, so let's move on
        
        return new_screenshot # [i] the screenshot exists and is new
    
    return False # [i] limit of attempts was reached


def display_intro(master: tk.Tk | tk.Toplevel = root):
    intro_win = tk.Toplevel(master)
    intro_win.focus_set()
    intro_win.resizable(False, False)
    intro_win.title("Meet Doom Map Guesser")
    
    if sys.platform == 'win32':
        intro_win.iconbitmap(ICON_PATH)
    
    tk_logo = ImageTk.PhotoImage(LOGO_PATH)
    logo_label = tk.Label(intro_win, image=tk_logo)
    
    about_1 = tk.Label(intro_win, text="Doom Map Guesser is the GeoGuesser of the DOOM series.")
    about_2 = tk.Label(intro_win, text="Enjoy this little game made by MF366! :D")
    about_3 = tk.Label(intro_win, text="Small note about what is considered a secret:")
    about_4 = tk.Label(intro_win, "The number of secrets are the number of sectors with Effect 9, whether they're acessible or not.")
    
    butt_github = tk.Button(intro_win, text='GitHub', command=lambda:
        simple_webbrowser.website("https://github.com/MF366-Coding/DoomMapGuesser"))
    butt_discord = tk.Button(intro_win, text='Discord Server', command=lambda:
        simple_webbrowser.website("https://discord.gg/HZnBRYTqvC"))
    butt_buy_coffee = tk.Button(intro_win, text="Donate <3", command=lambda:
        simple_webbrowser.website("https://buymeacoffee.com/mf366/"))
        
    logo_label.pack()
    about_1.pack()
    about_2.pack()
    about_3.pack()
    about_4.pack()
    butt_github.pack()
    butt_discord.pack()
    butt_buy_coffee.pack()


def display_screenshot():
    pass

'''
FIXME
tk_img = ImageTk.PhotoImage(scrapper.scrape_byte_contents())
label = tk.Label(root, image=tk_img)
label.pack()
'''



