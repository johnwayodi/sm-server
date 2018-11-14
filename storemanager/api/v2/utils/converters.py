"""
This Module contains functions that assist in conversion from one
data type to another
"""
from datetime import datetime


def date_to_string(date_object):
    """converts  date object to its string equivalent"""
    date_string = datetime.strftime(date_object, '%b %d, %Y')
    return date_string
