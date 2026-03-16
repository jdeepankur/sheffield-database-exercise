from html import escape
from typing import Iterable

def htmlClean(strings):
    if isinstance(strings, Iterable):
        return [escape(str(s)) for s in strings]
    elif isinstance(strings, str):
        return escape(strings)
    else:
        return None