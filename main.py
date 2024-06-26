import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import font
import random
import os
import sys
import simple_webbrowser
from PIL import ImageTk, Image
from core import level_db, scrapper
import sv_ttk
import ctypes
import math
import io

# pylint: disable=E1101
# pylint: disable=W0718
# pylint: disable=W0603

# [*] Enable high DPI scaling on Windows
if sys.platform == 'win32':
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    
    except Exception as e:
        print(f"Failed to set DPI awareness: {e}")

    # [*] Path to the font file
    font_path = os.path.join(os.path.dirname(__file__), 'assets', 'font.ttf')

    # [*] Verify that the font file exists
    if not os.path.exists(font_path):
        print(f"Font file '{font_path}' does not exist.")
        exit(1)

    # [*] Load the font
    ctypes.windll.gdi32.AddFontResourceW(str(font_path))

VERSION = 'v0.0.1 BETA'

CONFIG_PATH: str = os.path.join(os.path.dirname(__file__), ".config")
LOGO_PATH: str = os.path.join(os.path.dirname(__file__), "assets", "full_logo.png")
ICON_PATH: str = os.path.join(os.path.dirname(__file__), "assets", "full_logo.ico")
GAME_PH = 'Doom (1993) / The Ultimate Doom'
EPISODE_PH = 'E1: Knee-Deep in the Dead'
MAP_PH = 'E1M1: Hangar'
SECRETS_PH = 0

with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
    cache = f.read()
    cache = cache.split('\n')

root = tk.Tk()
root.title(f"Doom Map Guesser by MF366 - The GeoGuesser of DOOM ({VERSION})")
root.geometry(f'{int(cache[0])}x{int(cache[1])}')
root.resizable(True, False)

if sys.platform == 'win32':
    root.iconbitmap(ICON_PATH)

sv_ttk.set_theme(cache[2], root)
style = ttk.Style(root)

f1 = ttk.Frame(root)
f2 = ttk.Frame(f1)
f3 = ttk.Frame(f2)
f4 = ttk.Frame(f2)
f5 = ttk.Frame(f1)
f6 = ttk.Frame(f1)

img_label = ttk.Label(f3, text='Image not available.')

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

cur_screenshot = None
cur_settings = ['Norb', 'MF366', 'Zeca70', -1000]
cur_selections = [GAME_PH, EPISODE_PH, MAP_PH, SECRETS_PH]

game_var = tk.Variable(f4, list(database.keys()))
episode_var = tk.Variable(f4, list(database[cur_selections[0]].keys()))
maps_var = tk.Variable(f4, list(database[cur_selections[0]][cur_selections[1]].keys()))
number_of_secrets_var = tk.StringVar(f4, '0 Secrets')
points_var = tk.IntVar(root, 0)
max_points_var = tk.IntVar(root, 0)


def get_width_height_of_image(image: bytes, ratio: tuple[int, int] = (16, 9)):
    # [*] total number of pixels
    pixels: int = len(image) // 4

    # calculate height and width
    height: float = math.sqrt((ratio[1] / ratio[0]) * pixels)
    width: float = (ratio[0] / ratio[1]) * height

    # round to nearest integer
    height = round(height)
    width = round(width)
    
    return width, height


def choose_game_window(origin: ttk.Button, master: tk.Tk | tk.Toplevel = root):
    def _save_changes():
        try:
            index = game_listbox.curselection()[0]
            selected_text = game_listbox.get(index)
            
            cur_selections[0] = selected_text
            cur_selections[1] = list(database[cur_selections[0]].keys())[0]
            cur_selections[2] = list(database[cur_selections[0]][cur_selections[1]].keys())[0]
            
            origin.configure(text=selected_text)
            
            game_choice_win.destroy()
            
        except (tk.TclError, IndexError) as exc:
            mb.showerror("Doom Map Guesser - Error #1", f"You must select a game/WAD before hitting 'Comfirm'.\n{exc}")
           
    game_choice_win = tk.Toplevel(master)
    game_choice_win.focus_set()
    game_choice_win.geometry(f'{int(cache[3])}x{int(cache[4])}')
    game_choice_win.resizable(False, False)
    game_choice_win.title("Choose the correct game/WAD")
    
    if sys.platform == 'win32':
        game_choice_win.iconbitmap(ICON_PATH)
    
    game_listbox = tk.Listbox(game_choice_win, listvariable=game_var, bg='dark blue', fg='yellow', selectmode=tk.SINGLE, width=int(cache[5]), height=int(cache[6]))
    accept_butt = ttk.Button(game_choice_win, text='Confirm', command=_save_changes)
        
    game_listbox.pack()
    accept_butt.pack(pady=5)


def choose_episode_window(origin: ttk.Button, master: tk.Tk | tk.Toplevel = root):
    episode_var.set(list(database[cur_selections[0]].keys()))
    
    def _save_changes():
        try:
            index = episode_listbox.curselection()[0]
            selected_text = episode_listbox.get(index)
            
            cur_selections[1] = selected_text
            cur_selections[2] = list(database[cur_selections[0]][cur_selections[1]].keys())[0]
            
            origin.configure(text=selected_text)
            
            episode_choice_win.destroy()
            
        except tk.TclError as exc:
            mb.showerror("Doom Map Guesser - Error #1", f"You must select a game/WAD before hitting 'Comfirm'.\n{exc}")
           
    episode_choice_win = tk.Toplevel(master)
    episode_choice_win.focus_set()
    episode_choice_win.geometry(f'{int(cache[3])}x{int(cache[4])}')
    episode_choice_win.resizable(False, False)
    episode_choice_win.title(f"Choose the correct episode for {cur_selections[0]}")
    
    if sys.platform == 'win32':
        episode_choice_win.iconbitmap(ICON_PATH)
    
    episode_listbox = tk.Listbox(episode_choice_win, listvariable=episode_var, bg='dark blue', fg='yellow', selectmode=tk.SINGLE, width=int(cache[5]), height=int(cache[6]))
    accept_butt = ttk.Button(episode_choice_win, text='Confirm', command=_save_changes)
        
    episode_listbox.pack()
    accept_butt.pack(pady=5)
    

def choose_map_window(origin: ttk.Button, master: tk.Tk | tk.Toplevel = root):
    maps_var.set(list(database[cur_selections[0]][cur_selections[1]].keys()))
    
    def _save_changes():
        try:
            index = maps_listbox.curselection()[0]
            selected_text = maps_listbox.get(index)
            
            cur_selections[2] = selected_text
            
            origin.configure(text=selected_text)
            
            map_choice_win.destroy()
            
        except tk.TclError as exc:
            mb.showerror("Doom Map Guesser - Error #1", f"You must select a game/WAD before hitting 'Comfirm'.\n{exc}")
           
    map_choice_win = tk.Toplevel(master)
    map_choice_win.focus_set()
    map_choice_win.geometry(f'{int(cache[3])}x{int(cache[4])}')
    map_choice_win.resizable(False, False)
    map_choice_win.title(f"Choose the correct map for {cur_selections[1]}")
    
    if sys.platform == 'win32':
        map_choice_win.iconbitmap(ICON_PATH)
    
    maps_listbox = tk.Listbox(map_choice_win, listvariable=maps_var, bg='dark blue', fg='yellow', selectmode=tk.SINGLE, width=int(cache[5]), height=int(cache[6]))
    accept_butt = ttk.Button(map_choice_win, text='Confirm', command=_save_changes)
        
    maps_listbox.pack()
    accept_butt.pack(pady=5)


choose_game_butt = ttk.Button(f4, text=cur_selections[0], command=lambda:
    choose_game_window(choose_game_butt))
choose_episode_butt = ttk.Button(f4, text=cur_selections[1], command=lambda:
    choose_episode_window(choose_episode_butt))
choose_map_butt = ttk.Button(f4, text=cur_selections[2], command=lambda:
    choose_map_window(choose_map_butt))


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
        
        if screenshot_database[map_id] == []:
            return False
        
        new_screenshot: str = random.choice(screenshot_database[map_id])
        
        if new_screenshot == current_screenshot_link:
            continue # [i] same screenshot, so let's move on
        
        return new_screenshot # [i] the screenshot exists and is new
    
    return False # [i] limit of attempts was reached


def display_intro(master: tk.Tk | tk.Toplevel = root):
    intro_win = tk.Toplevel(master)
    intro_win.focus_set()
    intro_win.resizable(False, False)
    intro_win.title(f"Meet Doom Map Guesser ({VERSION})")
    
    if sys.platform == 'win32':
        intro_win.iconbitmap(ICON_PATH)
    
    logo = Image.open(LOGO_PATH)
    
    # [*] Resizing
    new_width = int(cache[8])
    original_width, original_height = logo.size
    aspect_ratio = original_height / original_width
    new_height = int(new_width * aspect_ratio)  # [i] Calculate the height based on the original aspect ratio
    resized_logo = logo.resize((new_width, new_height), Image.LANCZOS)
    
    intro_win.tk_logo = ImageTk.PhotoImage(resized_logo)
    logo_label = ttk.Label(intro_win, image=intro_win.tk_logo)
    
    about_1 = ttk.Label(intro_win, text=f"Doom Map Guesser {VERSION} is the GeoGuesser of the DOOM series.")
    about_2 = ttk.Label(intro_win, text="Enjoy this little game made by MF366! :D")
    about_3 = ttk.Label(intro_win, text="Small note about what is considered a secret:")
    about_4 = ttk.Label(intro_win, text="The number of secrets are the number of sectors with Effect 9, whether they're acessible or not.")
    
    butt_github = ttk.Button(intro_win, text='GitHub', command=lambda:
        simple_webbrowser.website("https://github.com/MF366-Coding/DoomMapGuesser"))
    butt_discord = ttk.Button(intro_win, text='Discord Server', command=lambda:
        simple_webbrowser.website("https://discord.gg/HZnBRYTqvC"))
    butt_buy_coffee = ttk.Button(intro_win, text="Donate <3", command=lambda:
        simple_webbrowser.website("https://buymeacoffee.com/mf366/"))
        
    logo_label.pack(pady=2)
    about_1.pack(pady=2)
    about_2.pack(pady=2)
    about_3.pack(pady=2)
    about_4.pack(pady=2)
    butt_github.pack(pady=5)
    butt_discord.pack(pady=5)
    butt_buy_coffee.pack(pady=5)


def display_screenshot(screenshot_link: str):
    # [!] I am assuming all screenshots are 16:9 which is NOT true
    
    print(screenshot_link)
    
    image_data = scrapper.scrape_byte_contents(screenshot_link)
    image_data_io = io.BytesIO(image_data)
    
    img = Image.open(image_data_io, "r")
    
    # [*] Resizing
    new_width = int(cache[9])
    original_width, original_height = img.size
    aspect_ratio = original_height / original_width
    new_height = int(new_width * aspect_ratio)  # [i] Calculate the height based on the original aspect ratio
    img_resized = img.resize((new_width, new_height), Image.LANCZOS)
    
    f3.tk_img = ImageTk.PhotoImage(img_resized)
    img_label.configure(text='', image=f3.tk_img)


def change_secret_amount_by_1(positive: bool):       
    if positive:
        a = 1
        
    else:
        a = -1
    
    num = number_of_secrets_var.get().split(' ')[0]        
    number_of_secrets_var.set(f"{int(num) + a} Secrets")


def reset_secret_amount():          
    number_of_secrets_var.set("0 Secrets")


secrets_label = ttk.Label(f4, textvariable=number_of_secrets_var)
secrets_plus_butt = ttk.Button(f4, text='+', command=lambda:
    change_secret_amount_by_1(True))
secrets_minus_butt = ttk.Button(f4, text='-', command=lambda:
    change_secret_amount_by_1(False))
secrets_reset_butt = ttk.Button(f4, text='Reset secrets', command=reset_secret_amount)


def generate_new_game(attempts: int = 10):
    global cur_screenshot, cur_selections, cur_settings
    
    game = pick_new_game_wad()
    episode = pick_new_episode(game)
    map_details = pick_new_map(game, episode)
    
    map_name = map_details[0]
    map_id = map_details[1]
    number_of_secrets = map_details[2]
    
    cur_screenshot = False
    
    for _ in range(attempts):
        if cur_screenshot is not False:
            break
        
        cur_screenshot = pick_new_screenshot(map_id, cur_screenshot, attempts)
    
    if cur_screenshot is False:
        mb.showerror('DoomMapGuesser - Error #3', f"Couldn't load a screenshot in {attempts * 2} attempts.")
        return
        
    cur_settings = [game, episode, map_name, number_of_secrets]
    cur_selections = [GAME_PH, EPISODE_PH, MAP_PH, SECRETS_PH]
    number_of_secrets_var.set('0 Secrets')
    
    choose_game_butt.configure(text=cur_selections[0])
    choose_episode_butt.configure(text=cur_selections[1])
    choose_map_butt.configure(text=cur_selections[2])

    # /-/ print(cur_screenshot)
    
    max_points_var.set(max_points_var.get() + 4)
    
    display_screenshot(cur_screenshot)
    

def guess_screenshot(attempts: int = 10):
    correct_guesses = 0
    
    num = number_of_secrets_var.get().split(' ')[0]
    cur_selections[3] = int(num)
    
    if cur_selections[3] < 0 or cur_selections[3] > 1000:
        mb.showerror('DoomMapGuesser - Error #2', "The number of secrets cannot be lower than 0 or greater than 1000.")
        return
    
    for index, setting in enumerate(cur_settings, 0):
        if cur_selections[index] == setting:
            correct_guesses += 1
    
    mb.showinfo("DoomMapGuesser - Final Results", f"Correct guesses: {correct_guesses}/4")
    
    points_var.set(points_var.get() + correct_guesses)
    
    generate_new_game(attempts)


def prevent_from_leaving(master: tk.Tk | tk.Toplevel = root):
    leave_confirmation = mb.askyesno("DoomMapGuesser by MF366", "Leaving already :(... Please stay a little longer... Will you?")

    if not leave_confirmation:
        master.destroy()


generate_butt = ttk.Button(f5, text="Generate new screenshot", command=lambda:
    generate_new_game(int(cache[7])))
guess_butt = ttk.Button(f5, text="Confirm guess", command=lambda:
    guess_screenshot(int(cache[7])))
leave_butt = ttk.Button(f5, text='Exit', command=prevent_from_leaving)

points_label = ttk.Label(f6, textvariable=points_var)
slash = ttk.Label(f6, text='/')
max_points_label = ttk.Label(f6, textvariable=max_points_var)

# [*] packing the rest of the elements
points_label.grid(column=0, row=0)
slash.grid(column=1, row=0)
max_points_label.grid(column=2, row=0)

img_label.pack()

choose_game_butt.pack(pady=2)
choose_episode_butt.pack(pady=2)
choose_map_butt.pack(pady=2)

secrets_plus_butt.pack(pady=2)
secrets_label.pack(pady=2)
secrets_minus_butt.pack(pady=2)
secrets_reset_butt.pack(pady=2)

generate_butt.pack(pady=2)
guess_butt.pack(pady=2)
leave_butt.pack(pady=2)

f6.pack()

f3.grid(column=0, row=0, padx=5, pady=2)
f4.grid(column=1, row=0, padx=5, pady=2)

f2.pack(pady=2)
f5.pack(pady=2)

f1.pack(pady=2)

display_intro()

style.configure("TButton", font=font.Font(root, family="Roboto", size=13, weight='normal', slant='roman'))
style.configure('TLabel', font=font.Font(root, family='Roboto', size=14, weight='bold', slant='roman'))

root.protocol("WM_DELETE_WINDOW", prevent_from_leaving)

root.mainloop()
