"""
# settings.py

**Handle the DoomMapGuesser settings.**
"""

import json
import sys
from typing import Any

# pylint: disable=W0718

class __CloseDialogError(Exception): ...


REGULAR_KEYS: tuple[str] = ("theme", "databases", "imageRatio", "imageWidth", "widthIsHeight", "checkUpdates", "excludeRule", "zoomBoost", "smallFonts")


class StrictModeError(Exception): ... # [<] teachers be like :| (this was such a stupid comment, gawdamn)


class __SettingsObjectCopy:
    def __init__(self, master: Any) -> None:
        """
        # __SettingsObjectCopy
        
        Serves as a copy of SettingsObject that doesn't allow for as much features.

        :param master: SettingsObject class
        """
        
        self._SETTINGS: dict[str, int | bool | str | float | list[list[str, str, str]] | None] = master._SETTINGS
        self.error_handler = master.error_handler
        self._MASTER = master
        
    def load(self) -> None:
        """"""
        
        self._MASTER.load()
        
        self._SETTINGS = self._MASTER._SETTINGS.copy()
        
    def save_settings(self, **kw) -> None:
        """
        ## save_settings
        Automatically save the settings using the default inner settings of the class.

        :param indent: how many spaces as indentation *(int, defaults to 4)*
        """
        
        self._MASTER._SETTINGS = self._SETTINGS
        self._MASTER.save_settings(**kw)
        del self

    @property
    def databases(self) -> list[list[str, str, str]]:
        return self._SETTINGS['databases']
    
    @databases.setter
    def databases(self, value: list[list[str, str, str]]):
        value.pop(0)
        self._SETTINGS['databases'] = value
    
    @databases.deleter
    def databases(self):
        self._SETTINGS['databases'].clear()
    
    @property
    def theme(self) -> str:
        match self._SETTINGS['theme']:
            case 1:
                return "light"
            
            case 2:
                return "dark"
            
            case _:
                return "auto"
    
    @theme.setter
    def theme(self, value: str | int):
        if isinstance(value, int):
            self._SETTINGS['theme'] = value
            return
        
        match value:
            case 'light':
                value = 1
                
            case 'dark':
                value = 2
                
            case _:
                value = 0
                
        self._SETTINGS['theme'] = value
    
    @property
    def image_ratio(self) -> bool:
        return self._SETTINGS['imageRatio']
    
    @image_ratio.setter
    def image_ratio(self, value: str):
        match value:
            case '16:9' | '1:1':
                print('Good image ratio.')
                
            case _:
                value = 'detect'
        
        self._SETTINGS['imageRatio'] = value
    
    @property
    def image_width(self) -> int:
        return self._SETTINGS['imageWidth']
    
    @image_width.setter
    def image_width(self, value: int):
        self._SETTINGS['imageWidth'] = value
        
    @property
    def use_width_as_height(self) -> bool:
        return self._SETTINGS['widthIsHeight']
    
    @use_width_as_height.setter
    def use_width_as_height(self, value: bool):
        self._SETTINGS['widthIsHeight'] = value
        
    @property
    def zoom_boost(self) -> float:
        return self._SETTINGS['zoomBoost']
    
    @zoom_boost.setter
    def zoom_boost(self, value: float):
        self._SETTINGS['zoomBoost'] = value
        
    @property
    def check_for_updates_on_startup(self) -> bool:
        return self._SETTINGS['checkUpdates']
    
    @check_for_updates_on_startup.setter
    def check_for_updates_on_startup(self, value: bool):
        self._SETTINGS['checkUpdates'] = value

    '''
    @property
    def autoupdate(self) -> bool:
        """
        # Levels of Auto Updating
        
        **Key name:** `autoUpdateLevel`

        0. **Always ask** (Default)
        1. **Always update**
        2. **Update if the latest is a major**
        3. **Never update**
        
        Auto Updating only works if **Check for Updates on Startup** (key name is `checkUpdates`) is enabled (set to `True`).
        
        Both Auto Updates and Check for Updates require a stable Internet connection.
        """
        
        return self._SETTINGS['autoUpdateLevel']
    
    @autoupdate.setter
    def autoupdate(self, value: bool):        
        if value < 0 or value > 3:
            value = 0 # [i] set to default
        
        self._SETTINGS['autoUpdateLevel'] = value
    '''
    
    @property
    def small_fonts(self) -> bool:
        return self._SETTINGS['smallFonts']
    
    @small_fonts.setter
    def small_fonts(self, value: bool):
        """
        # small_fonts
        
        **Key name:** `smallFonts`

        0. **Disabled**, which allows for the best UI experience
        1. **Enabled**, which allows for DoomMapGuesser to be played in smaller monitors
        """
        
        self._SETTINGS['smallFonts'] = value
        
    @property
    def exclude_rule_for_e3m1_e3m9(self, **kw) -> str | None:
        """
        # exclude_rule_for_e3m1_e3m9
        
        Whether to use **Hell Keep** or **Warrens** or both, even!
        
        :param obj: the object to save - if not specified, will save itself
        :param object: same as above but this one does not take priority
        
        Returns:
            str: either 'warrens', 'hellkeep' or 'both' depending on what the user chose *(None if set to show none)*
        """
        
        __obj = kw.get('obj', None)
        
        if __obj is None:
            __obj = kw.get('object', None)
        
        a: str | None = self._SETTINGS['excludeRule']
        
        if a not in ('warrens', 'hell_keep', 'both'):
            self._SETTINGS['excludeRule'] = None
            
        if __obj is None:
            self.save_settings()
            
        else:
            self.dump_settings(__obj)

        return self._SETTINGS['excludeRule']

    @exclude_rule_for_e3m1_e3m9.setter
    def exclude_rule_for_e3m1_e3m9(self, value: str | None):
        if value not in ('warrens', 'hell_keep', 'both'):
            value = None

        self._SETTINGS['excludeRule'] = value


class SettingsObject:
    class __SettingsObjectCopy:
        def __init__(self, master: Any) -> None:
            """
            # __SettingsObjectCopy
            
            Serves as a copy of SettingsObject that doesn't allow for as much features.

            :param master: SettingsObject class
            """
            
            self._SETTINGS: dict[str, int | bool | str | float | list[list[str, str, str]] | None] = master._SETTINGS
            self.error_handler = master.error_handler
            self._MASTER = master
            
        def load(self) -> None:
            """"""
            
            self._MASTER.load()
            
            self._SETTINGS = self._MASTER._SETTINGS.copy()
            
        def save_settings(self, **kw) -> None:
            """
            ## save_settings
            Automatically save the settings using the default inner settings of the class.

            :param indent: how many spaces as indentation *(int, defaults to 4)*
            """
            
            self._MASTER._SETTINGS = self._SETTINGS
            self._MASTER.save_settings(**kw)
            del self

        @property
        def databases(self) -> list[list[str, str, str]]:
            return self._SETTINGS['databases']
        
        @databases.setter
        def databases(self, value: list[list[str, str, str]]):
            value.pop(0)
            self._SETTINGS['databases'] = value
        
        @databases.deleter
        def databases(self):
            self._SETTINGS['databases'].clear()
        
        @property
        def theme(self) -> str:
            match self._SETTINGS['theme']:
                case 1:
                    return "light"
                
                case 2:
                    return "dark"
                
                case _:
                    return "auto"
        
        @theme.setter
        def theme(self, value: str | int):
            if isinstance(value, int):
                self._SETTINGS['theme'] = value
                return
            
            match value:
                case 'light':
                    value = 1
                    
                case 'dark':
                    value = 2
                    
                case _:
                    value = 0
                    
            self._SETTINGS['theme'] = value
        
        @property
        def image_ratio(self) -> bool:
            return self._SETTINGS['imageRatio']
        
        @image_ratio.setter
        def image_ratio(self, value: str):
            match value:
                case '16:9' | '1:1':
                    print('Good image ratio.')
                    
                case _:
                    value = 'detect'
            
            self._SETTINGS['imageRatio'] = value
        
        @property
        def image_width(self) -> int:
            return self._SETTINGS['imageWidth']
        
        @image_width.setter
        def image_width(self, value: int):
            self._SETTINGS['imageWidth'] = value
            
        @property
        def use_width_as_height(self) -> bool:
            return self._SETTINGS['widthIsHeight']
        
        @use_width_as_height.setter
        def use_width_as_height(self, value: bool):
            self._SETTINGS['widthIsHeight'] = value
            
        @property
        def zoom_boost(self) -> float:
            return self._SETTINGS['zoomBoost']
        
        @zoom_boost.setter
        def zoom_boost(self, value: float):
            self._SETTINGS['zoomBoost'] = value
            
        @property
        def check_for_updates_on_startup(self) -> bool:
            return self._SETTINGS['checkUpdates']
        
        @check_for_updates_on_startup.setter
        def check_for_updates_on_startup(self, value: bool):
            self._SETTINGS['checkUpdates'] = value

        '''
        @property
        def autoupdate(self) -> bool:
            """
            # Levels of Auto Updating
            
            **Key name:** `autoUpdateLevel`

            0. **Always ask** (Default)
            1. **Always update**
            2. **Update if the latest is a major**
            3. **Never update**
            
            Auto Updating only works if **Check for Updates on Startup** (key name is `checkUpdates`) is enabled (set to `True`).
            
            Both Auto Updates and Check for Updates require a stable Internet connection.
            """
            
            return self._SETTINGS['autoUpdateLevel']
        
        @autoupdate.setter
        def autoupdate(self, value: bool):        
            if value < 0 or value > 3:
                value = 0 # [i] set to default
            
            self._SETTINGS['autoUpdateLevel'] = value
        '''
        
        @property
        def small_fonts(self) -> bool:
            return self._SETTINGS['smallFonts']
        
        @small_fonts.setter
        def small_fonts(self, value: bool):
            """
            # small_fonts
            
            **Key name:** `smallFonts`

            0. **Disabled**, which allows for the best UI experience
            1. **Enabled**, which allows for DoomMapGuesser to be played in smaller monitors
            """
            
            self._SETTINGS['smallFonts'] = value
            
        @property
        def exclude_rule_for_e3m1_e3m9(self, **kw) -> str | None:
            """
            # exclude_rule_for_e3m1_e3m9
            
            Whether to use **Hell Keep** or **Warrens** or both, even!
            
            :param obj: the object to save - if not specified, will save itself
            :param object: same as above but this one does not take priority
            
            Returns:
                str: either 'warrens', 'hellkeep' or 'both' depending on what the user chose *(None if set to show none)*
            """
            
            __obj = kw.get('obj', None)
            
            if __obj is None:
                __obj = kw.get('object', None)
            
            a: str | None = self._SETTINGS['excludeRule']
            
            if a not in ('warrens', 'hell_keep', 'both'):
                self._SETTINGS['excludeRule'] = None
                
            if __obj is None:
                self.save_settings()
                
            else:
                self.dump_settings(__obj)

            return self._SETTINGS['excludeRule']

        @exclude_rule_for_e3m1_e3m9.setter
        def exclude_rule_for_e3m1_e3m9(self, value: str | None):
            if value not in ('warrens', 'hell_keep', 'both'):
                value = None

            self._SETTINGS['excludeRule'] = value

    def __init__(self, given_path: str, *_, handler: Any, initial_settings: dict[str, int | bool | str | float | list[list[str, str, str]]] | None = None, **kw) -> None:
        """
        # SettingsObject

        :param given_path: settings path *(str)*
        :param initial_settings: initial value for the settings *(dict; defaults to `None`)*
        If the param is None, the settings get loaded. Otherwise, it will use the initial ones until the user loads.
            
        By setting `strict=False`, you disabling strict mode for SettingsObject.
        
        Strict mode off will change this:
        - Accessing non existant key returns `None` instead of raising `KeyError`
        - It's possible to create new keys
        - Values associated with keys can be set to any type and not just the allowed ones
        """
        
        self._PATH = kw.get('overwrite', given_path)
        self.error_handler = handler
        self._SETTINGS: dict[str, int | bool | str | float | list[list[str, str, str]] | None] = initial_settings
        self._BE_STRICT = kw.get('strict', True)
        
        if initial_settings is None:
            self.load()
        
    def load(self) -> None:
        try:
            with open(self._PATH, 'r', encoding='utf-8') as f:
                self._SETTINGS = json.load(f)
                
        except FileNotFoundError as e:
            self.error_handler(44, f"FATAL ERROR\nSettings file could not be found!\n{e}")
            sys.exit()
            
        except PermissionError as e:
            self.error_handler(43, f"FATAL ERROR\nMissing permissions to read the settings file\n{e}")
            sys.exit()
            
        except UnicodeError as e:
            self.error_handler(42, f"FATAL ERROR\nSystem failed to translate the Unicode characters in the settings file\n{e}")
            sys.exit()
            
        except json.JSONDecodeError as e:
            self.error_handler(1, f"FATAL ERROR\nJSON file could not be parsed correctly.\n{e}")    
            sys.exit()
            
        except Exception as e:
            self.error_handler(3, f"FATAL ERROR\nUnknown error when attempting to parse the settings.\n{e}")
            sys.exit()
        
        it_happened = False # [i] variable that indicates whether an expected key is... gone... (this sounds stupid)
        
        for ek in REGULAR_KEYS:
            if ek not in self._SETTINGS:
                it_happened = True
                self.error_handler(2, f"FATAL ERROR\nMissing a key in the settings file.\nMissing key:\n'{ek}'")
                continue
            
            continue
        
        if it_happened:
            print('Program cannot handle missing key. Please review settings file.')
            sys.exit()   
        
    def save_settings(self, **kw) -> None:
        """
        ## save_settings
        Automatically save the settings using the default inner settings of the class.

        :param indent: how many spaces as indentation *(int, defaults to 4)*
        """
        
        self.dump_settings(self._SETTINGS, indent=kw.get('indent', 4))
            
    def dump_settings(self, obj: dict, **kw) -> None:
        """
        ## dump_settings
        Save settings using an outside object.

        :param obj: settings to save
        :param indent: how many spaces as indentation *(int, defaults to 4)*
        """
        
        obj = kw.get('overwrite', obj)
        
        try:
            with open(self._PATH, 'w', encoding='utf-8') as f:
                json.dump(obj, f, indent=kw.get("indent", 4))
        
        except FileNotFoundError as e:
            self.error_handler(44, f"FATAL ERROR\nSettings file could not be found!\n{e}")
            sys.exit()
            
        except PermissionError as e:
            self.error_handler(43, f"FATAL ERROR\nMissing permissions to write to the settings file\n{e}")
            sys.exit()
            
        except UnicodeError as e:
            self.error_handler(42, f"FATAL ERROR\nSystem failed to translate the Unicode characters\n{e}")
            sys.exit()
            
        except json.JSONDecodeError as e:
            self.error_handler(1, f"FATAL ERROR\nJSON file could not be parsed correctly\n{e}")    
            sys.exit()
            
        except Exception as e:
            self.error_handler(3, f"FATAL ERROR\nUnknown error when attempting to write to the settings\n{e}")
            sys.exit()

    @property
    def databases(self) -> list[list[str, str, str]]:
        return self._SETTINGS['databases']
    
    @databases.setter
    def databases(self, value: list[list[str, str, str]]):
        value.pop(0)
        self._SETTINGS['databases'] = value
    
    @databases.deleter
    def databases(self):
        self._SETTINGS['databases'].clear()
    
    @property
    def theme(self) -> str:
        match self._SETTINGS['theme']:
            case 1:
                return "light"
            
            case 2:
                return "dark"
            
            case _:
                return "auto"
    
    @theme.setter
    def theme(self, value: str | int):
        if isinstance(value, int):
            self._SETTINGS['theme'] = value
            return
        
        match value:
            case 'light':
                value = 1
                
            case 'dark':
                value = 2
                
            case _:
                value = 0
                
        self._SETTINGS['theme'] = value
    
    @property
    def image_ratio(self) -> bool:
        return self._SETTINGS['imageRatio']
    
    @image_ratio.setter
    def image_ratio(self, value: str):
        match value:
            case '16:9' | '1:1':
                print('Good image ratio.')
                
            case _:
                value = 'detect'
        
        self._SETTINGS['imageRatio'] = value
    
    @property
    def image_width(self) -> int:
        return self._SETTINGS['imageWidth']
    
    @image_width.setter
    def image_width(self, value: int):
        self._SETTINGS['imageWidth'] = value
        
    @property
    def use_width_as_height(self) -> bool:
        return self._SETTINGS['widthIsHeight']
    
    @use_width_as_height.setter
    def use_width_as_height(self, value: bool):
        self._SETTINGS['widthIsHeight'] = value
        
    @property
    def zoom_boost(self) -> float:
        return self._SETTINGS['zoomBoost']
    
    @zoom_boost.setter
    def zoom_boost(self, value: float):
        self._SETTINGS['zoomBoost'] = value
        
    @property
    def check_for_updates_on_startup(self) -> bool:
        return self._SETTINGS['checkUpdates']
    
    @check_for_updates_on_startup.setter
    def check_for_updates_on_startup(self, value: bool):
        self._SETTINGS['checkUpdates'] = value

    '''
    @property
    def autoupdate(self) -> bool:
        """
        # Levels of Auto Updating
        
        **Key name:** `autoUpdateLevel`

        0. **Always ask** (Default)
        1. **Always update**
        2. **Update if the latest is a major**
        3. **Never update**
        
        Auto Updating only works if **Check for Updates on Startup** (key name is `checkUpdates`) is enabled (set to `True`).
        
        Both Auto Updates and Check for Updates require a stable Internet connection.
        """
        
        return self._SETTINGS['autoUpdateLevel']
    
    @autoupdate.setter
    def autoupdate(self, value: bool):        
        if value < 0 or value > 3:
            value = 0 # [i] set to default
        
        self._SETTINGS['autoUpdateLevel'] = value
    '''
        
    @property
    def small_fonts(self) -> bool:
        return self._SETTINGS['smallFonts']
    
    @small_fonts.setter
    def small_fonts(self, value: bool):
        """
        # small_fonts
        
        **Key name:** `smallFonts`

        0. **Disabled**, which allows for the best UI experience
        1. **Enabled**, which allows for DoomMapGuesser to be played in smaller monitors
        """
        
        self._SETTINGS['smallFonts'] = value
        
    @property
    def exclude_rule_for_e3m1_e3m9(self, **kw) -> str | None:
        """
        # exclude_rule_for_e3m1_e3m9
        
        Whether to use **Hell Keep** or **Warrens** or both, even!
        
        :param obj: the object to save - if not specified, will save itself
        :param object: same as above but this one does not take priority
        
        Returns:
            str: either 'warrens', 'hell_keep' or 'both' depending on what the user chose *(None if set to show none)*
        """
        
        __obj = kw.get('obj', None)
        
        if __obj is None:
            __obj = kw.get('object', None)
        
        a: str | None = self._SETTINGS['excludeRule']
        
        if a not in ('warrens', 'hell_keep', 'both'):
            self._SETTINGS['excludeRule'] = None
            
        if __obj is None:
            self.save_settings()
            
        else:
            self.dump_settings(__obj)

        return self._SETTINGS['excludeRule']

    @exclude_rule_for_e3m1_e3m9.setter
    def exclude_rule_for_e3m1_e3m9(self, value: str | None):
        if value not in ('warrens', 'hell_keep', 'both'):
            value = None

        self._SETTINGS['excludeRule'] = value
        
    @property
    def copy(self):
        return self.__SettingsObjectCopy(self)
        
    def __getitem__(self, key: str) -> int | bool | str | float | list[str] | None:        
        if self._BE_STRICT:
            return self._SETTINGS[key] # [i] if there is error, there is error. this is how strict mode behaves.
        
        return self._SETTINGS.get(key, None) # [i] no error!! (strict off)
    
    def __setitem__(self, key: str, value: int | bool | float | str | list[str]):
        if self._BE_STRICT:
            if not isinstance(value, (int, str, float, list, bool)):
                raise ValueError('can only assign int, str, list[str] or boolean using SettingsObject.__setitem__')
            
            if key not in REGULAR_KEYS:
                raise KeyError('strict mode in SettingsObject does not allow for assigning new keys')
            
        self._SETTINGS[key] = value
