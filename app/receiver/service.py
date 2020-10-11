from .repo import receiver_by_id


def does_receiver_exist(receiver_id):
    return receiver_by_id(receiver_id) is not None
