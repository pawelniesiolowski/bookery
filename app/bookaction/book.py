from .models import BookAction, BookActionName


class Book:
    def __init__(self, events, *, book_id):
        self.book_id = book_id
        self.copies = Copies(0)
        self.apply_events(events)

    def apply_events(self, events):
        for event in events:
            if event.name == BookActionName.RECEIVE:
                self.copies = self.copies.add(Copies(event.copies))
            elif event.name == BookActionName.RELEASE:
                self.copies = self.copies.subtract(Copies(event.copies))

    def receive(self, copies):
        assert isinstance(copies, Copies),\
            'Copies must be instance of Copies class'
        self.copies = self.copies.add(copies)
        return BookAction(
            BookActionName.RECEIVE,
            copies.to_int(),
            book_id=self.book_id
        )

    def release(self, copies, *, receiver_id, comment=None):
        assert isinstance(copies, Copies),\
            'Copies must be instance of Copies class'
        self.copies = self.copies.subtract(copies)
        return BookAction(
            BookActionName.RELEASE,
            copies.to_int(),
            book_id=self.book_id,
            receiver_id=receiver_id,
            comment=comment
        )


class Copies:
    def __init__(self, num):
        num = num and int(num)
        if not isinstance(num, int) or num < 0:
            raise ValueError(
                'Egzemplarze muszą być liczbą większą lub równą zero'
            )
        self.num = num

    def add(self, copies):
        assert isinstance(copies, Copies),\
            'Copies must be instance of Copies class'
        return Copies(self.num + copies.to_int())

    def subtract(self, copies):
        assert isinstance(copies, Copies),\
            'Copies must be instance of Copies class'
        return Copies(self.num - copies.to_int())

    def to_int(self):
        return self.num
