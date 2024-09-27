import json
import requests

LOCAL = OFFLINE = 'local'


class StatusCodeNot200(Exception): ...


def __get_local_database(path: str) -> dict | int:
    try:
        with open(file=path, mode='r', encoding='utf-8') as f:
            return json.load(f)
        
    except UnicodeError:
        return 1
    
    except FileNotFoundError:
        return 2
    
    except json.JSONDecodeError:
        return 3
    
    except Exception as e:
        return (9, e)
    
    else:
        return 0


def __get_online_database(url: str) -> dict | int:
    try:
        response = requests.get(url=url, allow_redirects=False, timeout=1)
        
        if response.status_code != 200:
            raise StatusCodeNot200(f"status code is {response.status_code} and not 200")
        
        database: dict = response.json()
        
        return database
        
    except StatusCodeNot200:
        return 4
    
    except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError):
        return 5
    
    except (TimeoutError, requests.exceptions.Timeout):
        return 6
    
    except (requests.exceptions.InvalidURL, requests.exceptions.InvalidSchema, requests.exceptions.MissingSchema):
        return 7
    
    except Exception as e:
        return (10, e)


def get_database(source: str, mode: str = 'online') -> dict | int:
    match mode:
        case 'local' | 'offline':
            return __get_local_database(source)
        
        case _:
            return __get_online_database(source)
    
    return 8 # [!] Unknown error

