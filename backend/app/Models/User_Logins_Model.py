class User_Logins:
    def __init__(self, email, password, username):
        """
        Initialize a User_Logins object.

        :param email: The user's email (string).
        :param password: The user's password (string).
                       *Consider using hashing for real-world applications.*
        """
        self.email = email
        self.password = password
        self.username = username

    def to_dict(self):
        """
        Convert the User_Logins object to a dictionary.
        """
        return {
            "email": self.email,
            "password": self.password,
            "username": self.username
        }

    @staticmethod
    def from_dict(data):
        """
        Convert a dictionary to a User_Logins object.
        """
        return User_Logins(
            email=data.get("email"),
            password=data.get("password"),
            username=data.get("username")
        )

    def __repr__(self):
        return f"User_Logins(email='{self.email}', password='***', usernamer='{self.username}')"