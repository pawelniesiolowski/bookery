from flask_script import Command
import csv
from app.receiver.models import Receiver


class ReceiversMigrator(Command):
    def run(self):
        with open('data/receiver.csv', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                receiver = Receiver(row['name'], row['surname'])
                receiver.save()
                print(f'Inserted receiver: {receiver}')
