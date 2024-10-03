from typing import Any


DEFAULT_DB_URL = "https://raw.githubusercontent.com/MF366-Coding/DoomMapGuesser/main/.github/ss_db.json"
VERSION = 'v2.0.0'

def nullish_operator(value: Any, new_value: Any) -> Any:
    """
    # nullish_operator
    **Recreation of the GameMaker Studio 2's nullish operator (??) and self nullish operator (=??).**

    Example usage:
    ```
    username = nullish_operator(data.username, "INVALID USERNAME")
    ```
    """

    # [<] boy, do I love when I have to create functions for basic shit that should already have been made
    # [<] achstually, mf366, you literally contributed to Norb's NCapybaraLib by adding this exact feature
    # [<] achstually, shut yo ass up

    if value is None:
        return new_value

    return value


def clamp(value: int | float, m: int, n: int) -> int | float:
    if value < m:
        return m

    if value > n:
        return n

    return value
