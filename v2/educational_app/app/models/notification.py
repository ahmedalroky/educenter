from .user import User
from datetime import datetime

class Notification:
    def __init__(self, notification_id: int, user: User, message: str, timestamp: datetime = datetime.now(), read: bool = False):
        self.notification_id = notification_id
        self.user = user
        self.message = message
        self.timestamp = timestamp
        self.read = read

    def mark_as_read(self):
        self.read = True
