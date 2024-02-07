from .user import User

class Profile:
    def __init__(self, user: User, name: str, bio: str = None):
        self.user = user
        self.name = name
        self.bio = bio
