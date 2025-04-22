class User_Logins:
    def __init__(self, email, password, username, schedule, takenClasses = None, detail_Schedule = None, futureClasses = None):
        """
        Initialize a User_Logins object.

        :param email: The user's email (string).
        :param password: The user's password (string).
                       *Consider using hashing for real-world applications.*
        """
        self.email = email
        self.password = password
        self.username = username
        self.schedule = schedule
        self.takenClasses = takenClasses
        self.detail_Schedule = detail_Schedule
        self.futureClasses = futureClasses

    def to_dict(self):
        """
        Convert the User_Logins object to a dictionary.
        """
        return {
            "email": self.email,
            "password": self.password,
            "username": self.username,
            "schedule": self.schedule,
            "takenClasses": self.takenClasses,
            "detail_Schedule": self.detail_Schedule,
            "futureClasses": self.futureClasses
        }

    @staticmethod
    def from_dict(data):
        """
        Convert a dictionary to a User_Logins object.
        """
        return User_Logins(
            email=data.get("email"),
            password=data.get("password"),
            username=data.get("username"),
            schedule=data.get("schedule"),
            takenClasses=data.get("takenClasses"),
            detail_Schedule=data.get("detail_Schedule"),
            futureClasses=data.get("futureClasses")
        )

    def __repr__(self):
        return f"User_Logins(email='{self.email}', password='***', usernamer='{self.username}')"