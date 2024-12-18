"""
Copyright (C) 2021 SE Slash - All Rights Reserved
You may use, distribute and modify this code under the
terms of the MIT license.
You should have received a copy of the MIT license with
this file. If not, please write to: secheaper@gmail.com

"""

import os
import sys
import inspect
from bs4 import BeautifulSoup
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
import src.formattr as formatter


def test_sortList():
    """
    Checks the sortList function
    """
    arr = [{"price": "$10"}, {"price": "$20"}, {"price": "$0"}]
    ansArr = [{"price": "$0"}, {"price": "$10"}, {"price": "$20"}]
    revAnsArr = [{"price": "$20"}, {"price": "$10"}, {"price": "$0"}]
    assert formatter.sortList(arr, "pr", False) == ansArr
    assert formatter.sortList(arr, "pr", True) == revAnsArr


def test_sortList_empty():
    """
    Checks the sortList function with an empty list
    """
    arr = []
    ansArr = []
    assert formatter.sortList(arr, "price", False) == ansArr
    assert formatter.sortList(arr, "price", True) == ansArr


def test_sortList_no_prices():
    """
    Checks the sortList function when 'price' field is missing in the dictionaries
    """
    arr = [{"name": "item1"}, {"name": "item2"}, {"name": "item3"}]
    ansArr = [{"name": "item1"}, {"name": "item2"}, {"name": "item3"}]  # No change since no price field
    assert formatter.sortList(arr, "price", False) == ansArr
    assert formatter.sortList(arr, "price", True) == ansArr


def test_sortList_single_item():
    """
    Checks the sortList function with a single item in the list
    """
    arr = [{"price": "$10"}]
    ansArr = [{"price": "$10"}]
    assert formatter.sortList(arr, "price", False) == ansArr
    assert formatter.sortList(arr, "price", True) == ansArr


def test_sortList_non_numeric_price():
    """
    Checks the sortList function when price is not numeric (e.g. invalid price format)
    """
    arr = [{"price": "$ten"}, {"price": "$20"}, {"price": "$0"}]
    ansArr = [{"price": "$0"}, {"price": "$20"}, {"price": "$ten"}]
    assert formatter.sortList(arr, "pr", False) == ansArr



def test_sortList_invalid_sort_key():
    """
    Checks sortList function with an invalid sorting key
    """
    arr = [{"price": "$10"}, {"price": "$20"}, {"price": "$0"}]
    ansArr = [{"price": "$10"}, {"price": "$20"}, {"price": "$0"}]  # No change as the key is invalid
    assert formatter.sortList(arr, "invalid_key", False) == ansArr


def test_sortList_float_price():
    """
    Checks sortList function with float prices
    """
    arr = [{"price": "$10.5"}, {"price": "$20.25"}, {"price": "$0.99"}]
    ansArr = [{"price": "$0.99"}, {"price": "$10.5"}, {"price": "$20.25"}]
    revAnsArr = [{"price": "$20.25"}, {"price": "$10.5"}, {"price": "$0.99"}]
    assert formatter.sortList(arr, "pr", False) == ansArr
    assert formatter.sortList(arr, "pr", True) == revAnsArr



def test_sortList_large_numbers():
    """
    Checks the sortList function with large numbers
    """
    arr = [{"price": "$1000000"}, {"price": "$1000"}, {"price": "$500"}]
    ansArr = [{"price": "$500"}, {"price": "$1000"}, {"price": "$1000000"}]
    revAnsArr = [{"price": "$1000000"}, {"price": "$1000"}, {"price": "$500"}]
    assert formatter.sortList(arr, "pr", False) == ansArr
    assert formatter.sortList(arr, "pr", True) == revAnsArr



def test_sortList_descending_price():
    """
    Checks the sortList function to sort in descending order when price values are in descending order
    """
    arr = [{"price": "$1000"}, {"price": "$500"}, {"price": "$1000000"}]
    ansArr = [{"price": "$1000000"}, {"price": "$1000"}, {"price": "$500"}]
    assert formatter.sortList(arr, "pr", True) == ansArr



def test_sortList_case_insensitive_sorting():
    """
    Checks the sortList function for case insensitive sorting of the price field
    """
    arr = [{"price": "$20"}, {"price": "$100"}, {"price": "$50"}]
    ansArr = [{"price": "$20"}, {"price": "$50"}, {"price": "$100"}]  # Sorted in ascending order
    revAnsArr = [{"price": "$100"}, {"price": "$50"}, {"price": "$20"}]  # Sorted in descending order

    assert formatter.sortList(arr, "pr", False) == ansArr
    assert formatter.sortList(arr, "pr", True) == revAnsArr
