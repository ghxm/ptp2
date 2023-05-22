from ptp2.ptp2 import ParltrackRecord

class Dossier(ParltrackRecord):

    def __init__(self, record):

        self.events = []
        self.docs = []

        super().__init__(record)

        # rename activities to events
        if 'activities' in self.__dict__:
            self.events = self.activities
            del self.activities

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

        # get docs
        docs = object.__getattribute__(self, 'docs')

        # and event-only docs
        for e in self.events:
            if 'docs' in e:
                docs.append(e)

        return docs
