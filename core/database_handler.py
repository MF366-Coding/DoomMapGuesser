import json
from typing import Any
import requests
from PIL import Image
import io

# pylint: disable=W0718

class __CloseDialogError(Exception): ...

class StatusCodeNot200(Exception): ...


def __get_online_database(url: str, handler: Any) -> dict | int:
    try:
        response = requests.get(url=url, allow_redirects=False, timeout=1)
        
        if response.status_code != 200:
            raise StatusCodeNot200(f"status code is {response.status_code} and not 200")
        
        database: dict = response.json()
        
        return database
        
    except StatusCodeNot200:
        return handler(4, f"The Status Code of URL...\n\n{url}\n\n...is not 200, meaning DoomMapGuesser is unable to collect the database.")
    
    except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError):
        return handler(5, "Unable to connect via HTTP. This might be caused by a bad Internet connection.")
    
    except (TimeoutError, requests.exceptions.Timeout):
        return handler(6, f"The databases's URL...\n\n({url})\n\n...took too long to respond to the GET request.")
    
    except (requests.exceptions.InvalidURL, requests.exceptions.InvalidSchema, requests.exceptions.MissingSchema):
        return handler(7, f"The URL...\n\n({url})\n\n...is invalid.")
    
    except UnicodeError as e:
        return handler(17, f"Failed to translate the website's data to valid Unicode.\n{e}")
        
    except json.JSONDecodeError as e:
        return handler(18, f"Failed to decode JSON data from database stored at:\n\n{url}\n\nAre you sure this URL points to a JSON/raw JSON object?\n{e}")


def get_database(source: str, error_handler: Any, mode: str = 'online') -> dict | int:
    match mode:
        case 'local' | 'offline':
            return error_handler(45, "Local databases are not allowed anymore.")
        
        case _:
            return __get_online_database(source, error_handler)
    
    return error_handler(8, f"An unknown error happened when trying to access database located at:\n\n{source}\n\nMake sure the URL is correct.") # [!] Unknown error


def get_image(source: str, handler: Any, **kw):
    _ = kw.pop('url', None)
    _ = kw.pop('timeout', None)
    _ = kw.pop('allow_redirects', None)
    del _
    
    try:
        response = requests.get(url=source, allow_redirects=False, timeout=1.3)
        
        if response.status_code != 200:
            raise StatusCodeNot200(f"status code is {response.status_code} and not 200")
        
        img_bytes: bytes | bytearray = response.content

    except StatusCodeNot200:
        return handler(31, f"The Status Code of URL...\n\n{source}\n\n...is not 200, meaning DoomMapGuesser is unable to collect the image.")
    
    except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError):
        return handler(24, "Unable to connect via HTTP. This might be caused by a bad Internet connection.")
    
    except (TimeoutError, requests.exceptions.Timeout):
        return handler(21, f"The image's URL...\n\n({source})\n\n...took too long to respond to the GET request.")
    
    except (requests.exceptions.InvalidURL, requests.exceptions.InvalidSchema, requests.exceptions.MissingSchema):
        return handler(27, f"The URL...\n\n({source})\n\n...is invalid.")
    
    except Exception as e:
        return handler(28, f"Unknown error when trying to obtain the chosen image with URL:\n\n{source}\n\nError Details:\n{e}")
    
    try:
        image_data = io.BytesIO(img_bytes)
        image = Image.open(image_data, "r")
        
    except ValueError as e:
        return handler(26, f"The collected image is not in its RAW form or isn't even an image, therefore cannot be used by DoomMapGuesser.\n\nError Details:\n{e}")

    except Exception as e:
        return handler(28, f"Unknown error when trying to read the chosen image with URL with PIL:\n\n{source}\n\nError Details:\n{e}")
    
    return image
