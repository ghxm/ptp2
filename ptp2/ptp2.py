
import ijson
import lzip
from ptp2.utils import flatten_nested_keys, listify_nested_keys

def unzip_lizp(file_path, extract_to=None, return_stream=False):
    """
    Unzip a .lizp file and optionally return a file stream.

    Args:
        file_path (str): The path to the .lizp file.
        extract_to (str, optional): The directory where to extract the file. Defaults to None.
        return_stream (bool, optional): Whether to return a file stream. Defaults to False.

    Returns:
        file stream if open is True, None otherwise.

    Raises:
        ValueError: If extract_to is not set and open is False.
    """
    if extract_to is None and not open:
        raise ValueError("Either 'extract_to' must be set or 'open' must be True.")

    # unzip file
    if file_path.startswith('http'):
        in_memory_extract = lzip.decompress_url(file_path)
    else:
        in_memory_extract = lzip.decompress_file(file_path)


    # extract to file
    if extract_to is not None:
        # write to file in extract_to
        with open(extract_to, 'wb') as f:
            f.write(in_memory_extract)

    if return_stream:
        # return file stream
        return in_memory_extract


def stream_json(json_input, i = None, fun=lambda x: x, filter_fun = lambda x: True, limit=None, prefix='item'):
    """
    Stream a JSON file or a file stream.

    Args:
        json_input (str or file stream): The path to the JSON file or a file stream.
        i (int, optional): The index of the record to start streaming from. Defaults to None.
        fun (function, optional): A function to apply to each record. Defaults to identity function.
        filter_fun (function, optional): A function to filter records. Defaults to function that always returns True.
        limit (int, optional): The maximum number of records to stream. Defaults to None.
        prefix (str, optional): The prefix for the ijson.items function. Defaults to 'item'.

    Yields:
        The next record from the JSON file or file stream that passes the filter function, after applying the function `fun`.
    """

    print('streaming json')

    if isinstance(json_input, str):
        json_file = open(json_input, 'rb')
    else:
        json_file = json_input

    for j, record in enumerate(ijson.items(json_file, prefix)):

        if i is not None:
            if j < i:
                continue
            elif j > i:
                break

        if filter_fun(record):
            yield fun(record)

            if limit is not None:
                limit -= 1
                if limit == 0:
                    break
        else:
            continue

    if isinstance(json_input, str):
        json_file.close()

def load_json(json_input, i = None, fun=lambda x: x, filter_fun = lambda x: True, limit=None, prefix='item'):
    """
    Load a JSON file.

    Args:
        json_input (str or file stream): The path to the JSON file or a file stream.
        i (int, optional): The index of the record to start loading from. Defaults to None.
        fun (function, optional): A function to apply to each record. Defaults to identity function.
        filter_fun (function, optional): A function to filter records. Defaults to function that always returns True.
        limit (int, optional): The maximum number of records to load. Defaults to None.
        prefix (str, optional): The prefix for the ijson.items function. Defaults to 'item'.

    Returns:
        list: A list of records from the JSON file that pass the filter function, after applying the function `fun`.
    """

    return list(stream_json(json_input, i, fun, filter_fun, limit, prefix))


class ParltrackRecord(object):
    """Parltrack record."""

    # names of elements to exclude from DataFrame
    df_varnames_exclude = ['changes', 'meta']

    # keys of elements to flatten from single element lists to the element itself
    keynames_flatten = []

    # keys of elements to listify from single element to a list containing the element
    keynames_listify = []

    def __init__(self, record):
        """Initialize."""

        self.changes = []
        self.meta = {}

        # set all attributes from record dict
        for k, v in record.items():
            setattr(self, str(k).lower().replace(' ', '_'), v)

    def to_dict(self):
        """Convert to dict."""

        return {k: v for k, v in self.__dict__.items() if k not in ParltrackRecord.df_varnames_exclude}

    def to_df(self):
        """Convert to pandas DataFrame."""

        import pandas as pd

        return pd.DataFrame([self.to_dict()])

    def __repr__(self):
        """Repr."""

        return str(self.to_dict())

    def __str__(self):
        """Str."""

        return str(self.to_dict())


    def flatten_keys(self):
        """Flatten specified keys."""

        for key_path in self.keynames_flatten:
            flatten_nested_keys(self.__dict__, key_path)


    def listify_keys(self):
        """Listify specified keys."""

        for key_path in self.keynames_listify:
            listify_nested_keys(self.__dict__, key_path)

class ParltrackSubRecord(ParltrackRecord):
    """Parltrack sub-record."""

    def __init__(self, record):
        """Initialize."""

        super().__init__(record)

        del self.changes
        del self.meta
