from .book_action_model import BookActionName


class Book:
    def __init__(self, events):
        self.copies = 0
        self.apply_events(events)

    def apply_events(self, events):
        for event in events:
            if event.name == BookActionName.RECEIVE:
                self.copies += event.copies
