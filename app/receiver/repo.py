from .models import Receiver


def receivers_ordered_by_surname():
    return Receiver.query.filter(
        Receiver.deleted_at.is_(None)
    ).order_by(
        Receiver.surname.asc()
    ).all()


def receiver_by_id(receiver_id):
    return Receiver.query.get(receiver_id)


def does_receiver_exist(receiver):
    return Receiver.query.filter(
        Receiver.name == receiver.name,
        Receiver.surname == receiver.surname
    ).first() is not None
