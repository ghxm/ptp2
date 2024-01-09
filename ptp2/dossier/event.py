from ptp2 import ParltrackSubRecord
from ptp2.dossier.doc import Doc
from ptp2.utils import make_date
from datetime import date, datetime

class Event(ParltrackSubRecord):

    def __init__(self, record):

        super().__init__(record)

        # date parsing
        if isinstance(self.date, str):
            self.date_str = self.date
        elif isinstance(self.date, (date, datetime)):
            self.date_str = make_date(self.date).isoformat()
        else:
            self.date_str = None

        try:
            self.date = make_date(self.date)
        except:
            self.date = None

        # initialize doc objects
        self.docs = [Doc(d) for d in self.docs] if hasattr(self, 'docs') and self.docs is not None else []

    def has_docs(self):
        """Return True if event has docs."""
        return len(self.docs) > 0
