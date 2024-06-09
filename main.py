import tkinter as tk
import random
import os
import json
from PIL import ImageTk
from core import database, scrapper


ultimate_doom = {
    "E1: Knee-Deep in the Dead": {
        "E1M1: Hangar": [0, "3"],
        "E1M2: Nuclear Plant": [1, "5+"],
        "E1M3: Toxin Refinery": [2, "5+"],
        "E1M4: Command Control": [3, "3"],
        "E1M5: Phobos Lab": [4, "5+"],
        "E1M6: Central Processing": [5, "4"],
        "E1M7: Computer Station": [6, "4"],
        "E1M8: Phobos Anomaly": [7, "1"],
        "E1M9: Military Base": [8, "2"],
        "E1M10: Sewers": [9, "1"]
    },
    "E2: Shores of Hell": {
        "E2M1: Deimos Anomaly": [10, "4"],
        "E2M2: Containment Area": [11, "5+"],
        "E2M3: Refinery": [12, "5+"],
        "E2M4: Deimos Lab": [13, "5+"],
        "E2M5: Command Center": [14, "5+"],
        "E2M6: Halls of the Damned": [15, "3"],
        "E2M7: Spawning Vats": [16, "5+"],
        "E2M8: Tower of Babel": [17, "0"],
        "E2M9: Fortress of Mystery": [18, "1"]
    },
    "E3: Inferno": { # [!!] gotta fix this and add the other WADs/games
        "E2M1: Deimos Anomaly": [10, "4"],
        "E2M2: Containment Area": [11, "5+"],
        "E2M3: Refinery": [12, "5+"],
        "E2M4: Deimos Lab": [13, "5+"],
        "E2M5: Command Center": [14, "5+"],
        "E2M6: Halls of the Damned": [15, "3"],
        "E2M7: Spawning Vats": [16, "5+"],
        "E2M8: Tower of Babel": [17, "0"],
        "E2M9: Fortress of Mystery": [18, "1"]
    }
}


def load_database(url: str):
    return scrapper.scrape_json_contents(url)  


database = load_database()




def pick_new_screenshot(cur_screenshot: str):
    new_screenshot = cur_screenshot
    
    while new_screenshot == cur_screenshot:
        game = random.choice(database.)


root = tk.Tk()

f1 = tk.Frame(root)
f2 = tk.Frame(root)
f3 = tk.Frame(f2)
f4 = tk.Frame(f2)
f5 = tk.Frame(root)

tk_img = ImageTk.PhotoImage(scrapper.scrape_byte_contents())
label = tk.Label(root, image=tk_img)
label.pack()


