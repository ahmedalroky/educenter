class User:
    def __init__(self, user_id: int, username: str, email: str, password: str, role: str):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password = password  # Store hashed passwords only
        self.role = role
