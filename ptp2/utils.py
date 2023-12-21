from dateutil.parser import parse
from datetime import datetime, date

def make_date(input_date):
    """Convert a string or datetime object to a date object."""
    if isinstance(input_date, datetime):
        return input_date.date()
    elif isinstance(input_date, date):
        return input_date
    elif isinstance(input_date, str):
        return parse(input_date).date()
    else:
        raise TypeError("Input should be a string, date or datetime object")

def make_datetime(input_datetime, time=None):
    """Convert a string or date object to a datetime object."""
    if isinstance(input_datetime, datetime):
        return input_datetime
    elif isinstance(input_datetime, date):
        if time is None:
            return datetime.combine(input_datetime, datetime.min.time())
        else:
            return datetime.combine(input_datetime, time)
    elif isinstance(input_datetime, str):
        return parse(input_datetime)
    else:
        raise TypeError("Input should be a string, date or datetime object")

def flatten_nested_keys(obj, key_path):
    """
    Flatten specified keys in nested dictionaries.

    Args:
        obj (dict): The dictionary to flatten.
        key_path (str or list): The path to the key to flatten as a string or list of keys.

    Returns:
        dict: The dictionary with the specified keys flattened.
    """
    if isinstance(key_path, str):
        key_path = [key_path]  # Convert string to list

    key = key_path[0]

    if key in obj:
        if len(key_path) == 1:  # Base case: We've reached the key to flatten
            value = obj[key]
            if isinstance(value, (list, tuple)) and len(value) == 1:
                obj[key] = value[0]
        else:  # Recursive case: Traverse the next level of the dictionary
            flatten_nested_keys(obj[key], key_path[1:])

    return obj

def listify_nested_keys(obj, key_path):
    """
    Listify specified keys in nested dictionaries.

    Args:
        obj (dict): The dictionary to listify.
        key_path (list): The path to the key to listify as a list of keys.

    Returns:
        dict: The dictionary with the specified keys listified.
    """
    key = key_path[0]

    if key in obj:
        if len(key_path) == 1:  # Base case: We've reached the key to listify
            value = obj[key]
            if not isinstance(value, list):
                obj[key] = [value]
        else:  # Recursive case: Traverse the next level of the dictionary
            listify_nested_keys(obj[key], key_path[1:])

    return obj
