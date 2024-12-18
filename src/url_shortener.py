
"""
Copyright (c) 2021 Rohan Shah
This code is licensed under MIT license (see LICENSE.MD for details)

@author: Slash
"""

# Import Libraries
from pyshorteners import Shortener


def shorten_url(url):
    if url == '' or url is None:
        return url
    # Shorten the passed url
    s = Shortener()
    short_url = s.tinyurl.short(url)
    return short_url
