import tkinter as tk
from tkinter.font import Font
from tkinter import ttk
from typing import Any
import darkdetect
import pywinstyles
import random
import os
import sys
import simple_webbrowser
from PIL import ImageTk, Image
from core import utils_constants
from core.database_handler import get_database, get_image
from core.settings import SettingsObject


LATEST = None

CONFIG_PATH: str = os.path.join(os.path.dirname(__file__), "settings.json")
ASSETS_PATH = os.path.join(os.path.dirname(__file__), 'assets')
ICONS_PATH = os.path.join(ASSETS_PATH, 'icons')
LOGO_PATH: str = os.path.join(ASSETS_PATH, "full_logo.png")
THEME_PATH: str = os.path.join(ASSETS_PATH, 'sv.tcl')


def __send_responsive_dialog(*args):
    def __stop_dialog(*_):
        args[5].focus_force()

        try:
            __window.destroy()

        except Exception as e:
            raise __CloseDialogError(f'__stop_dialog failed to eliminate the message with id {id(__window)}') from e

    __window = tk.Toplevel(args[5])
    __window.focus_force()
    __window.resizable(False, False)

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

    __window.bind('<Button-1>', __stop_dialog)
    __window.bind('<Button-3>', __stop_dialog)

    __window.wait_window()


def __send_responsive_dialog_with_buttons(button_args: list[dict[str, Any]], *args):
    def __stop_dialog_hide_buttons(*_):
        args[5].focus_force()

        try:
            __window.destroy()

        except Exception as e:
            raise __CloseDialogError(f'__stop_dialog_hide_buttons failed to eliminate the message with id {id(__window)}') from e

    __window = tk.Toplevel(args[5])
    __window.focus_force()
    __window.resizable(False, False)

    apply_theme_to_titlebar(__window, settings)

    __old_icon = Image.open(os.path.join(ICONS_PATH, "universal", f"{args[0].lower()}.png"))

    __icon_img = resize_image(
        image=__old_icon,
        wanted_width=100,
    )

    __window.__icon = ImageTk.PhotoImage(image=__icon_img)

    __window.title(args[1])

    __frame = ttk.Frame(__window)
    __icon_widget = ttk.Label(__frame, image=__window.__icon)
    __label = ttk.Label(__frame, text=args[2], wraplength=args[3], font=args[4])

    __icon_widget.grid(column=0, row=0, padx=5, pady=5, ipadx=5, ipady=5)
    __label.grid(column=1, row=0, padx=5, pady=5, ipadx=5, ipady=5)

    __frame.pack(padx=5, pady=5, ipadx=5, ipady=5)

    __BUTTONS = []

    for __buttargs in button_args:
        __com = __buttargs.get('command', None)

        if __com is not None:
            match __com:
                case 'TYPE_DUPLICATE':
                    raise __InvalidButtonAction('action TYPE_DUPLICATE was removed for being useless')

                case 'TYPE_CLOSE':
                    __com = __stop_dialog_hide_buttons

                case _:
                    print('Special Command Received Well')

            __buttargs.pop('command')

            if __buttargs['type'] == 'PRIMARY':
                __BUTTONS.append(PrimaryButton(__window, command=__com, **__buttargs))

            else:
                __buttargs.pop('type')
                __BUTTONS.append(ttk.Button(__window, command=__com, **__buttargs))

            continue

        if __buttargs['type'] == 'PRIMARY':
            __BUTTONS.append(PrimaryButton(__window, **__buttargs))

        else:
            __buttargs.pop('type')
            __BUTTONS.append(ttk.Button(__window, **__buttargs))

    for __butt in __BUTTONS:
        __butt.pack(side='right', padx=5, pady=5, ipadx=5, ipady=5)

    __window.wait_window()


root = tk.Tk()
root.title(f'DoomMapGuesser by MF366 - {utils_constants.VERSION}')
root.geometry('900x700')


def handle_error(code: int, message: str, **kw) -> int:
    try:
        __send_responsive_dialog(kw.get('icon', 'error'), f"DoomMapGuesser - Error #{code}", f"=== Error #{code} ===\n{message}", kw.get('wraplenght', 400), kw.get('overwrite_font', SUBTITLE), kw.get('root_of', root))

    except FileNotFoundError as e:
        return handle_error(10, f"Invalid icon. A valid icon bust be the name of an image - without extension - that is inside:\nassets/icons/universal\n\n{e}")

    except __CloseDialogError as e:
        return handle_error(12, f"Failed to close dialog by left/right clicking.\n{e}")

    except KeyError as e:
        return handle_error(15, f"An invalid key was parsed.\n{e}")

    return code


def send_dialog(dtype: str, title: str, message: str, wraplenght: int = 400, root_of: tk.Tk | tk.Toplevel = root, **kw) -> int | None:
    try:
        __send_responsive_dialog(dtype, title, message, wraplenght, kw.get('overwrite_font', SUBTITLE), root_of)

    except FileNotFoundError as e:
        return handle_error(10, f"Invalid icon. A valid icon bust be the name of an image - without extension - that is inside:\nassets/icons/universal\n\n{e}")

    except __CloseDialogError as e:
        return handle_error(12, f"Failed to close dialog by left/right clicking.\n{e}")

    except KeyError as e:
        return handle_error(15, f"An invalid key was parsed.\n{e}")


def send_dialog_with_buttons(dtype: str, title: str, message: str, button_args: list[dict[str, Any]], wraplenght: int = 400, root_of: tk.Tk | tk.Toplevel = root, **kw) -> int | None:
    try:
        __send_responsive_dialog_with_buttons(button_args, dtype, title, message, wraplenght, kw.get('overwrite_font', SUBTITLE), root_of)

    except FileNotFoundError as e:
        return handle_error(9, f"Invalid icon. A valid icon bust be the name of an image - without extension - that is inside:\nassets/icons/universal\n\n{e}")

    except __CloseDialogError as e:
        return handle_error(13, f"Failed to close dialog.\n{e}")

    except __InvalidButtonAction:
        return handle_error(14, "Action 'TYPE_DUPLICATE' is no longer allowed when constructing a Button for a button dialog.")

    except KeyError as e:
        return handle_error(16, f"An invalid key was parsed.\nIt's very likely this was raised by a badly constructed Button.\n{e}")

    except tk.TclError as e:
        return handle_error(46, f"An invalid argument was parsed by tkinter.\nIt's very likely this was raised by a badly constructed Button.\n{e}")


settings = SettingsObject(CONFIG_PATH, handler=handle_error)


nl = utils_constants.nullish_operator


def autodetect_theme(configs: SettingsObject) -> None:
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


def apply_theme_to_titlebar(window: tk.Tk, configs: SettingsObject) -> None:
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

    resized_logo = image.resize((int(new_width), int(new_height)), resample, **kw)
    return resized_logo

autodetect_theme(settings)
MAIN_ICON_PATH: str = os.path.join(ASSETS_PATH, f"full_icon_{settings.theme}.ico")

if sys.platform == 'win32':
    root.iconbitmap(default=MAIN_ICON_PATH)

apply_theme_to_titlebar(root, settings)

sidebar = ttk.Frame(root, width=80)
main_frame = ttk.Frame(root, width=820)

database_bar = ttk.Frame(main_frame, height=80)
game_frame = ttk.Frame(main_frame)

HEADING1 = Font(root, family="SUSE ExtraBold", size=30)
HEADING2 = Font(root, family="SUSE Bold", size=22)
HEADING3 = Font(root, family='SUSE Semibold', size=17)
SUBTITLE = Font(root, family='SUSE Regular', size=12)
REGULAR_TEXT = Font(root, family='SUSE Regular', size=14)
LIGHT_TEXT = Font(root, family='SUSE Light', size=14)
XLIGHT_TEXT = Font(root, family='SUSE ExtraLight', size=14)
THIN_TEXT = Font(root, family='SUSE Thin', size=14)
BOLD_TEXT = Font(root, family='SUSE Medium', size=14)
PRIMARY_BUTTON = Font(root, family='SUSE Semibold', size=12, underline=False)
SECONDARY_BUTTON = Font(root, family='SUSE Light', size=12)

PLAY_ITEMS = ttk.Frame(game_frame)


class PrimaryButton(ttk.Button):
    def __init__(self, master = None, *, class_ = "", command = "", compound = "", cursor = "", default = "normal", image = "", name = ..., padding=..., state = "normal", takefocus = ..., text = "", textvariable = ..., underline = -1, width = "", **kw):
        kw.pop('type', None)
        super().__init__(master, class_=class_, command=command, compound=compound, cursor=cursor, default=default, image=image, name=name, padding=padding, state=state, style='Primary.TButton', takefocus=takefocus, text=text, textvariable=textvariable, underline=underline, width=width)


class ImportantFrame(ttk.Frame):
    def __init__(self, master = None, *, border = ..., borderwidth = ..., class_ = "", cursor = "", height = 0, name = ..., padding = ..., relief = ..., takefocus = "", width = 0):
        super().__init__(master, border=border, borderwidth=borderwidth, class_=class_, cursor=cursor, height=height, name=name, padding=padding, relief=relief, style='Important.TFrame', takefocus=takefocus, width=width)


class ImportantLabel(ttk.Label):
    def __init__(self, master = None, *, anchor = ..., background = "", border = ..., borderwidth = ..., class_ = "", compound = "", cursor = "", image = "", justify = ..., name = ..., padding = ..., relief = ..., state = "normal", takefocus = "", text = "", textvariable = ..., underline = -1, width = "", wraplength = ...):
        super().__init__(master, anchor=anchor, background=background, border=border, borderwidth=borderwidth, class_=class_, compound=compound, cursor=cursor, image=image, justify=justify, name=name, padding=padding, relief=relief, state=state, style="Important.TLabel", takefocus=takefocus, text=text, textvariable=textvariable, underline=underline, width=width, wraplength=wraplength)


class __CloseDialogError(Exception): ...
class __InvalidButtonAction(Exception): ...


CUR_DB = None
CUR_DATA: list[str] | None = None
PH_DATA: list[str] | None = None
POINTS: int = 0
GEN_SF: int = 0
CUR_IMG_LINK = None


def generate_new_map_data(**kw) -> list[str] | int:
    db: Database = kw.get('database', CUR_DB)

    warrens: list[str] | None = db.warrens
    hell_keep: list[str] | None = db.hell_keep

    # [*] 1st Case: WARRENS and HELL_KEEP are undefined
    # [i] this code assumes Database.verify() has been ran
    if warrens is None and hell_keep is None:
        return db.generate()

    # [*] 2nd Case: WARRENS and HELL_KEEP can be both shown - in this case, we don't need to do anything
    if settings.exclude_rule_for_e3m1_e3m9 == 'both':
        return db.generate()

    is_warrens = False
    is_hk = False
    data = None

    # [*] 3rd Case: we loop around 20 times, which should be enough to get rid of WARRENS and HELL_KEEP generated data
    # [i] ofc that if we get valid data before the last loop, we end it, duh?!
    for _ in range(kw.get('attempts', 20)): # [<] just as a safety measure to make sure it all goes right :)
        data: list[str] = db.generate()

        # [<] messy code incoming but it works, so leave it there please :blush:
        if data == warrens:
            is_warrens = True
            is_hk = False

        elif data == hell_keep:
            is_warrens = False
            is_hk = True

        else:
            is_warrens = False
            is_hk = False

        match settings.exclude_rule_for_e3m1_e3m9:
            case 'warrens':
                if is_hk is False:
                    break

            case 'hell_keep':
                if is_warrens is False:
                    break

            case None | 'null' | 'none':
                if is_hk is False and is_warrens is False:
                    break

            case _:
                data = None
                continue

    if data is None:
        return handle_error(52, "Failed to get an image that respects the chosen exclusion rule for HELL_KEEP and WARRENS.")

    return data


def generate_new_image(data: list[str], **kw) -> str:
    """
    # generate_new_image

    Get an image from the selected data.

    :param database: overwrite for CUR_DB *(should be of type Database)*

    Returns:
        str: the link to the new image
    """

    db: Database = kw.get('database', CUR_DB)

    x = random.choice(db.structure[data[0]][data[1]][data[2]]['screenshots'].remove(CUR_IMG_LINK))
    return x


def get_selected_image(img_link: str, **kw) -> Image.Image | int:
    return get_image(img_link, handle_error, **kw)


def generate_new_round(*_, first: dict[str, Any] = None, second: dict[str, Any] = None, third: dict[str, Any] = None):
    global CUR_DATA, GEN_SF, CUR_IMG_LINK

    # [<] ik one letter vars are not good but screw it
    if first is None:
        a = generate_new_map_data()

    else:
        a = generate_new_map_data(**first)

    if isinstance(a, int):
        return # [!?] Cancel the operation, since an error happened

    if second is None:
        b = generate_new_image(a)

    else:
        b = generate_new_image(b, **second)

    if third is None:
        c = get_selected_image(b)

    else:
        c = get_selected_image(b, **third)

    GEN_SF += 4
    CUR_DATA = a
    CUR_IMG_LINK = b
    PLAY_ITEMS.cur_img = resize_image(c, settings.image_width, settings.use_width_as_height, settings.image_ratio)


def update_game_widgets(scope: str) -> int:
    if scope == 'game':
        PLAY_ITEMS.selected_episode.set(list(CUR_DB.structure[PLAY_ITEMS.selected_game.get()].keys())[0])
        PLAY_ITEMS.episode_ch.set_menu(PLAY_ITEMS.selected_episode.get(), *list(CUR_DB.structure[PLAY_ITEMS.selected_game.get()].keys()))
        scope = 'episode'

    if scope == 'episode':
        PLAY_ITEMS.selected_map.set(list(CUR_DB.structure[PLAY_ITEMS.selected_game.get()][PLAY_ITEMS.selected_episode.get()].keys())[0])
        PLAY_ITEMS.map_ch.set_menu(PLAY_ITEMS.selected_map.get(), *list(CUR_DB.structure[PLAY_ITEMS.selected_game.get()][PLAY_ITEMS.selected_episode.get()].keys()))
        
    return 0


def zoom_in_image():
    img_display = tk.Toplevel(root)
    img_display.geometry(f'{int(PLAY_ITEMS.cur_img.size[0] * settings.zoom_boost)}x{int(PLAY_ITEMS.cur_img.size[1] * settings.zoom_boost)}')
    img_display.title('Zoom In on Generated Image')
    img_display.resizable(False, False)
    
    img_display.image = resize_image(PLAY_ITEMS.cur_img, settings.image_width * settings.zoom_boost, settings.use_width_as_height, settings.image_ratio)
    
    img_display.actual_tk = ImageTk.PhotoImage(img_display.image)
    
    img_display.actual_tk.pack()
    
    img_display.bind('<Button-1>', img_display.destroy)
    img_display.bind('<Button-3>', img_display.destroy)
    
    img_display.wait_window()
    

def setup_play_screen():
    global CUR_DATA, POINTS, GEN_SF, CUR_IMG_LINK, PH_DATA

    PH_DATA = [random.randint(10, 99) for _ in range(3)]
    CUR_DATA = PH_DATA.copy()
    CUR_IMG_LINK = None
    GEN_SF = 0
    POINTS = 0

    PLAY_ITEMS.selected_game = tk.StringVar(PLAY_ITEMS, list(CUR_DB.structure.keys())[0])
    PLAY_ITEMS.selected_episode = tk.StringVar(PLAY_ITEMS, list(CUR_DB.structure[PLAY_ITEMS.selected_game.get()].keys())[0])
    PLAY_ITEMS.selected_map = tk.StringVar(PLAY_ITEMS, list(CUR_DB.structure[PLAY_ITEMS.selected_game.get()][PLAY_ITEMS.selected_episode.get()].keys())[0])
    PLAY_ITEMS.selected_secrets = tk.IntVar(PLAY_ITEMS, 0)

    PLAY_ITEMS.headframe = ttk.Frame(PLAY_ITEMS)
    PLAY_ITEMS.heading = ttk.Label(PLAY_ITEMS.headframe, text='Play', font=HEADING1, justify='left')
    PLAY_ITEMS.f0 = ttk.Frame(master=PLAY_ITEMS.headframe)
    PLAY_ITEMS.f1 = ttk.Frame(PLAY_ITEMS.headframe)
    
    PLAY_ITEMS.mainframe = ttk.Frame(PLAY_ITEMS)
    PLAY_ITEMS.f2 = ttk.Frame(PLAY_ITEMS.mainframe)
    PLAY_ITEMS.f3 = ttk.Frame(PLAY_ITEMS.mainframe)
    PLAY_ITEMS.f4 = ttk.Frame(PLAY_ITEMS)
    PLAY_ITEMS.f5 = ttk.Frame(PLAY_ITEMS.f4)
    PLAY_ITEMS.f6 = ttk.Frame(PLAY_ITEMS.f4)
    PLAY_ITEMS.f7 = ttk.Frame(PLAY_ITEMS.f4)
    PLAY_ITEMS.f8 = ttk.Frame(PLAY_ITEMS.f4)
    PLAY_ITEMS.f9 = ttk.Frame(PLAY_ITEMS.f8)

    PLAY_ITEMS.database_label = ttk.Label(PLAY_ITEMS.f0, text="Using the defualt database." if CUR_DB.source == utils_constants.DEFAULT_DB_URL else f'Using database with link <{CUR_DB.source}>!')
    PLAY_ITEMS.points_label = ttk.Label(PLAY_ITEMS.f1, text=f'Points: {POINTS} / {GEN_SF}')

    if settings.use_width_as_height:
        PLAY_ITEMS.f2.configure(height=int(settings.image_width + 20))

    else:
        PLAY_ITEMS.f2.configure(width=int(settings.image_width + 20))

    PLAY_ITEMS.cur_img = resize_image(
            Image.open(os.path.join(ASSETS_PATH, 'errors', 'image_none_yet.png')),
            settings.image_width,
            settings.use_width_as_height,
            settings.image_ratio
        )

    PLAY_ITEMS.cur_tk_img = ImageTk.PhotoImage(PLAY_ITEMS.cur_img)
    

    PLAY_ITEMS.img_widget = ttk.Button(PLAY_ITEMS.f2, image=PLAY_ITEMS.cur_tk_img, command=zoom_in_image)

    PLAY_ITEMS.generation_butt = ttk.Button(PLAY_ITEMS.f3, text="Generate", command=generate_new_round)

    PLAY_ITEMS.guessing_butt = ttk.Button(PLAY_ITEMS.f3, text='Guess', command=lambda:
        handle_error(11, "Not implemented yet!", icon='warning')) # TODO

    PLAY_ITEMS.game_label = ttk.Label(PLAY_ITEMS.f5, text='Game', font=BOLD_TEXT)
    PLAY_ITEMS.episode_label = ttk.Label(PLAY_ITEMS.f6, text='Episode', font=BOLD_TEXT)
    PLAY_ITEMS.map_label = ttk.Label(PLAY_ITEMS.f7, text='Map', font=BOLD_TEXT)
    PLAY_ITEMS.secrets_label = ttk.Label(PLAY_ITEMS.f8, text='Secrets', font=BOLD_TEXT)
    
    PLAY_ITEMS.game_ch = ttk.OptionMenu(PLAY_ITEMS.f5, PLAY_ITEMS.selected_game, PLAY_ITEMS.selected_game.get(), *list(CUR_DB.structure.keys()), command=lambda:
        update_game_widgets('game'))
    PLAY_ITEMS.episode_ch = ttk.OptionMenu(PLAY_ITEMS.f6, PLAY_ITEMS.selected_episode, PLAY_ITEMS.selected_episode.get(), *list(CUR_DB.structure[PLAY_ITEMS.selected_game.get()].keys()), command=lambda:
        update_game_widgets('episode'))
    PLAY_ITEMS.map_ch = ttk.OptionMenu(PLAY_ITEMS.f7, PLAY_ITEMS.selected_map, PLAY_ITEMS.selected_map.get(), *list(CUR_DB.structure[PLAY_ITEMS.selected_game.get()][PLAY_ITEMS.selected_episode.get()].keys()))
    
    PLAY_ITEMS.secrets_minus = ttk.Button(PLAY_ITEMS.f9, text='-', command=lambda:
        PLAY_ITEMS.selected_secrets.set(PLAY_ITEMS.selected_secrets.get() + 1))
    PLAY_ITEMS.secrets_reset = ttk.Button(PLAY_ITEMS.f9, textvariable=PLAY_ITEMS.selected_secrets, command=lambda:
        PLAY_ITEMS.selected_secrets.set(0))
    PLAY_ITEMS.secrets_plus = ttk.Button(PLAY_ITEMS.f9, text='+', command=lambda:
        PLAY_ITEMS.selected_secrets.set(PLAY_ITEMS.selected_secrets.get() + 1))
    
    # [*] Upper
    PLAY_ITEMS.heading.pack(ipadx=5, ipady=5, padx=5, pady=5)
    PLAY_ITEMS.database_label.pack(ipadx=5, ipady=5, padx=5, pady=5)
    PLAY_ITEMS.points_label.pack(ipadx=5, ipady=5, padx=5, pady=5)
    PLAY_ITEMS.f0.pack(ipadx=5, ipady=5, padx=5, pady=5)
    PLAY_ITEMS.f1.pack(ipadx=5, ipady=5, padx=5, pady=5)
    
    # [*] Image
    PLAY_ITEMS.img_widget.pack(ipadx=5, ipady=5, padx=5, pady=5)
    PLAY_ITEMS.f2.grid(column=0, row=0, padx=5, pady=10, ipadx=5, ipady=10)
    
    # [*] Generate/Guess
    PLAY_ITEMS.generation_butt.pack(ipadx=5, ipady=10, padx=5, pady=10)
    PLAY_ITEMS.guessing_butt.pack(ipadx=5, ipady=10, padx=5, pady=10)
    PLAY_ITEMS.f3.grid(column=1, row=0, padx=5, pady=10, ipadx=5, ipady=10)
    
    # [*] Game
    PLAY_ITEMS.game_label.pack(ipadx=5, ipady=5, padx=5, pady=5)
    PLAY_ITEMS.game_ch.pack(ipadx=5, ipady=5, padx=5, pady=5)
    PLAY_ITEMS.f5.grid(column=0, row=0, padx=5, pady=5, ipadx=5, ipady=5)
    
    # [*] Episode
    PLAY_ITEMS.episode_label.pack(ipadx=5, ipady=5, padx=5, pady=5)
    PLAY_ITEMS.episode_ch.pack(ipadx=5, ipady=5, padx=5, pady=5)
    PLAY_ITEMS.f6.grid(column=1, row=0, padx=5, pady=5, ipadx=5, ipady=5)
    
    # [*] Map
    PLAY_ITEMS.map_label.pack(ipadx=5, ipady=5, padx=5, pady=5)
    PLAY_ITEMS.map_ch.pack(ipadx=5, ipady=5, padx=5, pady=5)
    PLAY_ITEMS.f7.grid(column=0, row=1, padx=5, pady=5, ipadx=5, ipady=5)
    
    # [*] Secrets
    PLAY_ITEMS.secrets_label.pack(ipadx=5, ipady=5, padx=5, pady=5)
    PLAY_ITEMS.secrets_minus.grid(column=0, row=0, padx=5, pady=5, ipadx=5, ipady=5)
    PLAY_ITEMS.secrets_reset.grid(column=1, row=0, padx=5, pady=5, ipadx=5, ipady=5)
    PLAY_ITEMS.secrets_plus.grid(column=2, row=0, padx=5, pady=5, ipadx=5, ipady=5)
    PLAY_ITEMS.f9.pack(ipadx=5, ipady=5, padx=5, pady=5)
    PLAY_ITEMS.f8.grid(column=1, row=1, padx=5, pady=5, ipadx=5, ipady=5)
    
    # [*] Play Screen
    PLAY_ITEMS.headframe.pack(ipadx=5, ipady=5, padx=5, pady=5)
    PLAY_ITEMS.mainframe.pack(ipadx=5, ipady=5, padx=5, pady=5)
    PLAY_ITEMS.f4.pack(ipadx=5, ipady=5, padx=5, pady=5)
    
    PLAY_ITEMS.pack()


class Database:
    def __init__(self, source: str):
        """
        # Database

        :param source: the URL from where the database should be aquired *(str)*
        """

        self._SOURCE = source
        self._DB = {}
        self._INDEX = None

    def search(self) -> bool:
        """
        # Database.search

        Search for the stored database in the list of databases.

        Returns:
            bool: the database was found
        """

        for index, db in enumerate(DATABASES, 0):
            if db == self:
                self._INDEX = index
                return True # [i] it's in

        return False # [i] it's NOT in

    def obtain(self) -> None | int:
        """
        # Database.obtain

        ## Alias
        - **Database.get** *(previously named this way, but the name was changed and get became the alias)*

        Returns:
            int: the error code *(None if the database was correctly obtained)*
        """

        db = get_database(self._SOURCE, handle_error)

        if isinstance(db, int):
            return db

        self._DB = db

    get = obtain

    def use(self) -> None:
        """
        # Database.use

        Use this database as the one to generate screenshots from.

        ## Alias
        - **Database.set_as_primary**
        """

        global CUR_DB, PH_DATA, CUR_DATA, POINTS, GEN_SF

        self.add()
        self.search()
        
        CUR_DB = self
        
        setup_play_screen()

    set_as_primary = use

    def add(self, **kw) -> None:
        """
        # Database.add

        Add or update the database information in the used DBs.

        :param index: the index to insert in

        ## Alias
        - **Database.append**
        """
        
        if kw.get('index', 1) == 0 and self._SOURCE != utils_constants.DEFAULT_DB_URL:
            return handle_error(50, "Cannot replace the Default Database in the list.", icon='error')

        if self.search():
            DATABASES[self._INDEX] = self

        else:
            if kw.get('index', -2) == -2:
                DATABASES.append(self)

            else:
                DATABASES.insert(kw.get('index'), self)

    append = add

    def remove(self) -> int:
        """
        # Database.remove

        Remove the database information in the used DBs and set the used DB to the default if this one is being used.

        ## Alias
        - **Database.pop**

        Returns:
            int: error code *(number 0 if everything went right)*
        """

        global CUR_DB

        if not self.search():
            return handle_error(49, "This database is not being used by DoomMapGuesser in any way.")

        if self._INDEX == 0:
            return handle_error(48, "Cannot remove the Default Database.", icon='error')

        if CUR_DB == self:
            CUR_DB = DATABASES[0]

        try:
            DATABASES.pop(self._INDEX)

        except IndexError as e:
            return handle_error(51, f"Unable to remove the database from use.\n{e}")

        else:
            return 0

    pop = remove

    def verify(self) -> int:
        """
        # Database.verify

        Use 3 different rulesets to verify whether this database is usable or not.

        Returns 0 if it is.

        It is possible the database has badly placed screenshots but these are indentified during the game. They are not removed and neither is the database.

        ## Alias
        - **Database.validate**

        Returns:
            int: error code associated with what makes this DB invalid *(integer 0 means the DB is valid)*
        """

        # [!?] Rule 1: if WARRENS is defined, HELL_KEEP must also be defined
        w = self._DB.get('WARRENS', None)
        hk = self._DB.get('HELL_KEEP', None)

        if [w, hk].count(None) == 1:
            self._DB = {}
            return handle_error(19, "The database structure is not correct. WARRENS and HELL_KEEP require each other, so the user might leave both undefined or define both, but cannot define only one of them.")

        # [!?] Rule 2: overall structure should be correct
        if self._DB.get('struct', None) is None:
            self._DB = {}
            return handle_error(20, "Missing the whole main component in the database. The key matching the main component is 'struct'.")

        if not isinstance(self._DB['struct'], dict):
            self._DB = {}
            return handle_error(20, "The main component of the database must be a dictionary (or object, using JSOn terms).")

        for k1, v1 in self._DB['struct'].items(): # [i] going thru the games
            if not isinstance(k1, str) or not isinstance(v1, dict):
                self._DB = {}
                return handle_error(20, "Games should be strings and should match a dictionary (episodes).")

            for k2, v2 in v1.items(): # [i] going thru the episodes
                if not isinstance(k2, str) or not isinstance(v2, dict):
                    self._DB = {}
                    return handle_error(20, "Episodes should be strings and should match a dictionary (maps).")

                for k3, v3 in v2.items(): # [i] going thru the maps
                    if not isinstance(k3, str) or not isinstance(v3, dict):
                        self._DB = {}
                        return handle_error(20, "In the databases, DOOM maps should be strings and should match a dictionary (individual map info).")

                    if not isinstance(v3.get('screenshots'), list) or not all(isinstance(item, str) for item in v3['screenshots']):
                        self._DB = {}
                        return handle_error(22, "A list of URLs pointing to screenshots must be the match for the key 'screenshots'.")

                    if len(v3['screenshots']) < 1:
                        self._DB = {}
                        return handle_error(23, "A list of URLs pointing to screenshots must be the match for the key 'screenshots'.\nIn this case, it is empty, which is not allowed.")

                    secrets = v3.get('secrets')

                    if not isinstance(secrets, int):
                        self._DB = {}
                        return handle_error(22, "An integer between 0 and 99, both ends included, must be the match for the key 'secrets'.")

                    if -1 < secrets < 100:
                        print('good range')

                    else:
                        self._DB = {}
                        return handle_error(25, "An integer between 0 and 99, both ends included, must be the match for the key 'secrets'.")

        # [!?] Rule 3: WARRENS and HELL_KEEP are pointing to valid maps
        if w is None or hk is None:
            w_list = w.split('///')
            hk_list = hk.split('///')

            # [!?] Rule 3.1: Lenght is 3 - game, episode, map
            if len(w_list) != 3:
                self._DB = {}
                return handle_error(19, "WARRENS should be a string in format:\nGAME///EPISODE///MAP")

            if len(hk_list) != 3:
                self._DB = {}
                return handle_error(19, "HELL_KEEP should be a string in format:\nGAME///EPISODE///MAP")

            # [!?] Rule 3.2: Game, episode and map are valid
            if self._DB['struct'].get(w_list[0], None) is None:
                self._DB = {}
                return handle_error(19, "WARRENS is pointing to an invalid game.")

            if self._DB['struct'][w_list[0]].get(w_list[1], None) is None:
                self._DB = {}
                return handle_error(19, f"WARRENS is poiting to an invalid episode inside of game {w_list[0]}")

            if self._DB['struct'][w_list[0]][w_list[1]].get(w_list[2], None) is None:
                self._DB = {}
                return handle_error(19, f"WARRENS is poiting to an invalid map inside of game {w_list[0]}, episode {w_list[1]}")

            # --

            if self._DB['struct'].get(w_list[0], None) is None:
                self._DB = {}
                return handle_error(19, "HELL_KEEP is pointing to an invalid game.")

            if self._DB['struct'][w_list[0]].get(w_list[1], None) is None:
                self._DB = {}
                return handle_error(19, f"HELL_KEEP is poiting to an invalid episode inside of game {w_list[0]}")

            if self._DB['struct'][w_list[0]][w_list[1]].get(w_list[2], None) is None:
                self._DB = {}
                return handle_error(19, f"HELL_KEEP is poiting to an invalid map inside of game {w_list[0]}, episode {w_list[1]}")

        return 0 # [i] it cool
        # [!] NOTE: it's possible a database has wrong images - however, images are tested at the time they are generated

    validate = verify

    def generate(self) -> list[str]:
        """
        # Database.generate

        ## Alias
        - **Database.gen**

        Returns:
            list[str]: a list of 3 generated choices in order - Game, Episode, Map
        """

        choices: list[str] = [
            random.choice(list(self._DB['struct'].keys()))
        ]

        choices.append(random.choice(self._DB['struct'][choices[0]]))
        choices.append(random.choice(self._DB['struct'][choices[0]][choices[1]]))
        # [<] no need to append the details, that can be done manually after

        return choices.copy()

    gen = generate

    @property
    def database(self) -> dict | None:
        """
        # Database.database

        ## Alias
        - **Database.db**

        Returns:
            dict: the database a dict *(None means the database hasn't been obtained or is invalid)*
        """

        if not self._DB:
            return None

        return self._DB

    db: property = database

    @property
    def structure(self) -> dict | None:
        """
        # Database.structure

        ## Alias
        - **Database.struct**
        - **Database.database['struct']**

        Returns:
            dict: the inner game/ep./map structure in the database *(None means the database hasn't been obtained or is invalid)*
        """

        if not self._DB:
            return None

        return self._DB['struct']

    struct: property = structure

    @property
    def warrens(self) -> list[str] | None:
        """
        # Database.warrens

        ## Alias
        - **Database.e3m9**
        - **Database.database['WARRENS']**

        Returns:
            list[str]: the value associated with WARRENS as a split str *(None if WARRENS is undefined - if this happens, HELL_KEEP should also be undefined)*

        ## Note
        If you want the unsplit version, just join the list by `///`, leaving you with the following code:
        ```
        # assuming var is where you saved the value of Database.warrens
        new_var = '///'.join(var)
        ```
        """

        if not self._DB or 'WARRENS' not in self._DB:
            return None

        return self._DB['WARRENS'].split('///')

    e3m9: property = warrens

    @property
    def hell_keep(self) -> list[str] | None:
        """
        # Database.hell_keep

        ## Alias
        - **Database.e3m1**
        - **Database.database['HELL_KEEP']**

        Returns:
            list[str]: the value associated with HELL_KEEP as a split str *(None if HELL_KEEP is undefined - if this happens, WARRENS should also be undefined)*

        ## Note
        If you want the unsplit version, just join the list by `///`, leaving you with the following code:
        ```
        # assuming var is where you saved the value of Database.hell_keep
        new_var = '///'.join(var)
        ```
        """

        if not self._DB or 'HELL_KEEP' not in self._DB:
            return None

        return self._DB['HELL_KEEP'].split('///')

    e3m1: property = hell_keep

    @property
    def index(self) -> int | None:
        """
        # Database.index

        Returns:
            int: the index that matches the database in DATABASES *(None if not in DATABASES)*
        """

        if not self.search():
            return None

        return self._INDEX

    @property
    def source(self) -> str:
        """
        # Database.source

        ## Alias
        - **Database.url**
        - **Database.link**

        Returns:
            str: the URL where the database was downloaded from
        """

        return self._SOURCE

    url = link = source # [<] "OMG, code so ugly. lil bro literally triple assigned ew." shut the frick up!

    def __eq__(self, value) -> bool:
        if isinstance(value, dict):
            return self._DB == value

        return self._DB == value.database

    def __ne__(self, value) -> bool:
        return not self.__eq__(value)

    def __str__(self) -> str:
        return str(self._DB)

    def __len__(self) -> int:
        return len(self._DB)

    def __iter__(self):
        return self._DB.__iter__()

    def __getitem__(self, item) -> Any:
        return self._DB[item]

    def __setitem__(self, item, value) -> None:
        self._DB[item] = value


def add_database(source: str, *_, index: int | None = None) -> Database | bool:
    new_database = Database(source=source)
    new_database.get()

    if new_database.database is None:
        return False

    if new_database.verify() != 0:
        return False

    new_database.search() # [i] this can be omited as .add() already does a search
    new_database.add(index=index)

    return Database


DATABASES: list[Database] = []

for i in settings.databases:
    add_database(i)

if not add_database(utils_constants.DEFAULT_DB_URL, index=0):
    handle_error(47, "CRITICAL ERROR\nUnable to obtain/verify the default database.")
    sys.exit()

DATABASES[0].use()


# [*] Sidebar Buttons
play_img = resize_image(
    Image.open(os.path.join(ICONS_PATH, settings.theme, 'play.png')),
    50,
    aspect_ratio='1:1'
)

play_tk = ImageTk.PhotoImage(play_img)

play_butt = ttk.Button(sidebar, image=play_tk, width=50, command=setup_play_screen)

play_butt.grid(column=0, row=0, ipadx=5, ipady=5, padx=5, pady=5)

database_bar.pack()
game_frame.pack()

sidebar.grid(column=0, row=0)
main_frame.grid(column=1, row=0)

# [!?] https://github.com/rdbende/Sun-Valley-ttk-theme (Sun Valley theme)
# [<] Credits to rdbende
root.tk.call("source", os.path.join(THEME_PATH))
style = ttk.Style(root)
style.theme_use(f"sun-valley-{settings.theme}")
style.configure('TLabel', font=REGULAR_TEXT)
style.configure('TButton', font=SECONDARY_BUTTON)
style.configure('Primary.TButton', font=PRIMARY_BUTTON, foreground='#5bcff1' if settings.theme == 'dark' else '#040929')
style.configure('Important.TFrame', background='#f17b7b' if settings.theme == 'dark' else "#5a0606")
style.configure('Important.TLabel', font=BOLD_TEXT, foreground='#000000' if settings.theme == 'dark' else "#ffffff")
style.configure('TEntry', font=SUBTITLE, background='#9c9c9c' if settings.theme == 'dark' else "#0e0e0e", foreground='#000000' if settings.theme == 'dark' else '#ffffff')

settings.save_settings()

root.mainloop()
