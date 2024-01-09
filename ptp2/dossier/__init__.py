from ptp2 import ParltrackRecord
from ptp2.dossier.event import Event
from ptp2.dossier.doc import Doc

class Dossier(ParltrackRecord):

    keynames_flatten = [['procedure', 'stage_reached'],
                        ['procedure', 'reference'],
                        ['procedure', 'title'],
                        ['procedure', 'type'],
                        ['procedure', 'subtype']]

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
        self.events = [Event(e) for e in object.__getattribute__(self, 'events')] if object.__getattribute__(self, 'events') is not None else []


    def __getattribute__(self, item):
        """Get attribute."""

        if item == 'procedure_reference':
            return self.get_procedure_reference()
        elif item == 'procedure_type':
            return self.__dict__.get('procedure', {}).get('type', None)
        elif item == 'docs':
            return self.get_docs()
        elif item == 'events':
            # return events sorted by date
            return self.get_events()
        else:
            return object.__getattribute__(self, item)

    def get_procedure_reference(self):
        """Get procedure reference."""

        return object.__getattribute__(self, 'procedure').get('reference', None)

    def get_events (self):
        """Get events."""
        events = object.__getattribute__(self, 'events')
        return sorted(events, key=lambda x: x.date if hasattr(x, 'date') else 99) if events is not None else []

    def get_docs(self, include_events_with_docs=True):
        """Get docs."""

        # TODO docs are events for now since they have the same attributes
        docs = [Event(doc) for doc in object.__getattribute__(self, 'docs')] if object.__getattribute__(self, 'docs') is not None else []

        # add event-only docs
        if include_events_with_docs:
            # make sure they are not in the docs list already
            [docs.append(e) for e in self.events if e.has_docs() and (e.get('type', None) is not None and (e.get('type') not in [d.get('type', None) for d in docs]) or e.get('type', None) is None)]

        return docs


