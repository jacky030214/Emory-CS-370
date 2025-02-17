class Professor:
    def __init__(self, name, email, ratemyprof_score, ratemyprof_tags=None):
        """
        :param name: Name of the professor (string).
        :param email: Email address of the professor (string).
        :param ratemyprof_score: Rating score from RateMyProf (float or int).
        :param ratemyprof_tags: List of tags from RateMyProf (e.g., ["Tough Grader", "Inspirational"]).
        """
        self.name = name
        self.email = email
        self.ratemyprof_score = ratemyprof_score
        # Default to an empty list if not provided
        self.ratemyprof_tags = ratemyprof_tags if ratemyprof_tags else []

    def to_dict(self):
        """
        Convert the Professor object into a dictionary (suitable for MongoDB insertion).
        """
        return {
            "name": self.name,
            "email": self.email,
            "ratemyprof_score": self.ratemyprof_score,
            "ratemyprof_tags": self.ratemyprof_tags
        }

    @staticmethod
    def from_dict(data):
        """
        Convert a dictionary (e.g., from MongoDB) back into a Professor object.
        """
        return Professor(
            name=data.get("name"),
            email=data.get("email"),
            ratemyprof_score=data.get("ratemyprof_score"),
            ratemyprof_tags=data.get("ratemyprof_tags", [])
        )

    def __repr__(self):
        return (
            f"Professor(name='{self.name}', "
            f"email='{self.email}', "
            f"ratemyprof_score={self.ratemyprof_score}, "
            f"ratemyprof_tags={self.ratemyprof_tags})"
        )