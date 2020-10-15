from .models import Receiver


def receivers_ordered_by_surname():
    return Receiver.query.filter(
        Receiver.deleted_at.is_(None)
    ).order_by(
        Receiver.surname.asc()
    ).all()


def receiver_by_id(receiver_id):
    return Receiver.query.get(receiver_id)


def receiver_by_name(name, surname):
    return Receiver.query.filter(
        Receiver.name == name,
        Receiver.surname == surname
    ).first()
