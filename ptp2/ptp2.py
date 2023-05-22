"""Main module."""
import ijson

def stream_json(json_file, i = None, fun=lambda x: x, filter_fun = lambda x: True, limit=None, prefix='item'):
    """Stream a JSON file."""

    with open(json_file, 'r') as f:
        for j, record in enumerate(ijson.items(f, prefix)):

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

def load_json(json_file, i = None, fun=lambda x: x, filter_fun = lambda x: True, limit=None, prefix='item'):
    """Load a JSON file."""

    return list(stream_json(json_file, i, fun, filter_fun, limit, prefix))


class ParltrackRecord(object):
    """Parltrack record."""

    def __init__(self, record):
        """Initialize."""

        self.changes = []
        self.meta = {}

        # set all attributes from record dict
        for k, v in record.items():
            setattr(self, k, v)


