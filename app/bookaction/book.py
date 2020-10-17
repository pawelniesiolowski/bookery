from .models import BookAction, BookActionName


class Book:
    def __init__(self, events, *, book_id):
        assert isinstance(book_id, int) and book_id > 0, \
            'Book id must be number greater than zero'
        self.book_id = book_id
        self.copies = Copies(0)
        self.apply_events(events)
        self.events = events

    def apply_events(self, events):
        for event in events:
            if event.name == BookActionName.RECEIVE:
                self.copies = self.copies.add(Copies(event.copies))
            elif event.name == BookActionName.RELEASE:
                self.copies = self.copies.subtract(Copies(event.copies))
            elif event.name == BookActionName.SELL:
                self.copies = self.copies.subtract(Copies(event.copies))
            else:
                raise ValueError(f'Event with invalid name: #{event.name}, \
was applied to book with id: #{self.book_id}')

    def receive(self, copies):
        validate_copies(copies)
        self.copies = self.copies.add(copies)
        return BookAction(
            BookActionName.RECEIVE,
            copies.to_int(),
            book_id=self.book_id
        )

    def release(self, copies, *, receiver_id, comment=None):
        validate_copies(copies)
        self.copies = self.copies.subtract(copies)
        return BookAction(
            BookActionName.RELEASE,
            copies.to_int(),
            book_id=self.book_id,
            receiver_id=receiver_id,
            comment=comment
        )

    def sell(self, copies):
        validate_copies(copies)
        self.copies = self.copies.subtract(copies)
        return BookAction(
            BookActionName.SELL,
            copies.to_int(),
            book_id=self.book_id
        )

    def sell_released(self, copies, *, release_id):
        validate_copies(copies)
        for event in self.events:
            if event.id == release_id:
                return self.do_sell_released(event, copies)
        raise ValueError(f'Release action with id {release_id} does not exist')

    def do_sell_released(self, action, copies):
        sold = copies.to_int()
        if action.copies > sold:
            action.copies = action.copies - sold
            action.save_in_transaction()
            return BookAction(
                BookActionName.SELL,
                sold,
                book_id=self.book_id
            )
        elif action.copies == sold:
            action.delete_in_transaction()
            return BookAction(
                BookActionName.SELL,
                sold,
                book_id=self.book_id
            )
        else:
            msg = 'Selled copies must be greater or equals to released copies'
            raise ValueError(msg)


class Copies:
    def __init__(self, num):
        assert isinstance(num, int) and num >= 0, \
            'Copies must greater than or equals zero'
        self.num = num

    def add(self, copies):
        validate_copies(copies)
        return Copies(self.num + copies.to_int())

    def subtract(self, copies):
        validate_copies(copies)
        return Copies(self.num - copies.to_int())

    def to_int(self):
        return self.num


def validate_copies(copies):
    assert isinstance(copies, Copies) and copies.to_int() > 0, \
        'Copies for action must be greater than zero'
