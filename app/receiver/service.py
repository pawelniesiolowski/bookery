"""Interface for accessing Receiver's data from external modules"""


from typing import Dict, Optional
from . import repo


def does_receiver_exist(receiver_id: int) -> bool:
    return repo.receiver_by_id(receiver_id) is not None


def get_receiver(receiver_id: int) -> Optional[Dict]:
    receiver = repo.receiver_by_id(receiver_id)
    if receiver is None:
        return None
    return receiver.format()
