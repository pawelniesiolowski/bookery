from .receiver_model import Receiver


class ReceiverRepo:
    def get_all_ordered_by_surname(self):
        return Receiver.query.filter(
            Receiver.deleted_at.is_(None)
        ).order_by(
            Receiver.surname.asc()
        ).all()

    def get_by_id(self, receiver_id):
        return Receiver.query.get(receiver_id)

    def does_receiver_exist(self, receiver):
        return Receiver.query.filter(
            Receiver.name == receiver.name
            and Receiver.surname == receiver.surname
        ).count() > 0
