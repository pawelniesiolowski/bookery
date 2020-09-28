from .receiver_model import Receiver


class ReceiverRepo:
    def getAllOrderedBySurname(self):
        return Receiver.query.filter(
            Receiver.deleted_at.is_(None)
        ).order_by(
            Receiver.surname.asc()
        ).all()

    def getById(self, receiver_id):
        return Receiver.query.get(receiver_id)
