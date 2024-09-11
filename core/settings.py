"""
# settings.py

**Handle the DoomMapGuesser settings.**
"""

import json

UNRETRIEVABLE = None


class SettingsObject:
    def __init__(self, given_path: str, *_, initial_settings: dict[str, int | bool | str | list[str]] | None, **kw) -> None:
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
        self._SETTINGS: dict[str, int | bool | str | list[str]] = initial_settings
        self._BE_STRICT = kw.get('strict', True)
        
        if initial_settings is None:
            self.load()
        
    def load(self) -> None:
        with open(self._PATH, 'r', encoding='utf-8') as f:
            self._SETTINGS = json.load(f)

    def dump_settings(self, obj: dict, **kw) -> None:
        if 'overwrite' in kw:
            obj = kw['overwrite']
        
        with open(self._PATH, 'w', encoding='utf-8') as f:
            json.dump(obj, f, indent=kw.get("indent", 4))
            
    @property
    def databases(self) -> list[str]:
        return self._SETTINGS['databases']
    
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
    def offline_mode(self) -> bool:
        return self._SETTINGS['offlineMode']
    
    @offline_mode.setter
    def offline_mode(self, value: bool):
        self._SETTINGS['offlineMode'] = value
    
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
    def check_for_updates_on_startup(self) -> bool:
        return self._SETTINGS['checkUpdates']
    
    @check_for_updates_on_startup.setter
    def check_for_updates_on_startup(self, value: bool):
        self._SETTINGS['checkUpdates'] = value
        
    @property
    def display_app_intro(self) -> bool:
        return self._SETTINGS['intro']
    
    @display_app_intro.setter
    def display_app_intro(self, value: bool):
        self._SETTINGS['intro'] = value
        
    @property
    def skip_downloaded_db_warning(self) -> bool:
        return self._SETTINGS['skipDatabaseWarning']
    
    @skip_downloaded_db_warning.setter
    def skip_downloaded_db_warning(self, value: bool):
        self._SETTINGS['skipDatabaseWarning'] = value

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
        
    def __getitem__(self, key: str) -> int | bool | str | list[str] | None:        
        if self._BE_STRICT:
            return self._SETTINGS[key]
        
        return self._SETTINGS.get(key, UNRETRIEVABLE)
    
    def __setitem__(self, key: str, value: int | bool | str | list[str]):
        if self._BE_STRICT:
            if not isinstance(value, (int, str, list, bool)):
                raise ValueError('can only assign int, str, list[str] or boolean using SettingsObject.__setitem__')
            
            if key not in ("theme", "offlineMode", "databases", "imageRatio", "imageWidth", "widthIsHeight", "checkUpdates", "intro", "skipDatabaseWarning", "autoUpdateLevel"):
                raise KeyError('strict mode in SettingsObject does not allow for assigning new keys')
            
        self._SETTINGS[key] = value
