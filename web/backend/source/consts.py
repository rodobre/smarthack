#!/usr/bin/python3
import os

def helper_get_path(f):
    return os.path.dirname(os.path.realpath(f))

proj_path = helper_get_path(__file__)
page_title = "Empty page"
