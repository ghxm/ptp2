from ptp2 import ParltrackRecord
from ptp2.dossier.event import Event

class Dossier(ParltrackRecord):

    keynames_flatten = ['stage_reached',
                        'reference',
                        'title',
                        'type',
                        'subtype']

    keynames_listify = [['procedure', 'subject']]

    def __init__(self, record):

        self.events = []
        self.docs = []
        self.committees = []

        super().__init__(record)

        # rename activities to events
        if 'activities' in self.__dict__:
            self.events = self.activities
            del self.activities

        # initialize event objects
        self.events = [Event(e) for e in self.events] if self.events is not None else []


    def __getattribute__(self, item):
        """Get attribute."""

        if item == 'procedure_reference':
            return self.get_procedure_reference()
        elif item == 'docs':
            return self.get_docs()
        else:
            return object.__getattribute__(self, item)

    def get_procedure_reference(self):
        """Get procedure reference."""

        return object.__getattribute__(self, 'procedure').get('reference', None)

    def get_docs(self):
        """Get docs."""

        docs = []

        # and event-only docs
        for e in self.events if self.events is not None else []:
            if hasattr(e, 'docs') and e.docs is not None and len(e.docs) > 0:
                docs.append(e)

        return docs


