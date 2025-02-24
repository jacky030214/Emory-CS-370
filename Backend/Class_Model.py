class Class_Model:
    def __init__(self,
                 class_id,
                 class_name,
                 recurring,
                 credit_hours,
                 prereqs=None,
                 requirement_designation=None,
                 campus=None,
                 class_desc=None):
        """
        :param class_id: Unique identifier for the class (string or int)
        :param class_name: Descriptive name/title of the class (string)
        :param recurring: Indicates the recurring pattern (e.g., "every Spring/Fall")
        :param credit_hours: Number of credit hours for the class (int)
        :param prereqs: List of prerequisite class IDs/numbers (list of strings/ints)
        :param requirement_designation: List of requirement designations, e.g. ["Core", "Elective"] (list of strings)
        :param campus: The campus where the class is offered (e.g., "OX" or "EM")
        :param class_desc: A textual description of the class (string)
        """
        self.class_id = class_id
        self.class_name = class_name
        self.recurring = recurring
        self.credit_hours = credit_hours
        self.prereqs = prereqs if prereqs else []
        self.requirement_designation = requirement_designation if requirement_designation else []
        self.campus = campus
        self.class_desc = class_desc

    def to_dict(self):
        """
        Convert the ClassModel object into a dictionary (suitable for MongoDB insertion).
        """
        return {
            "class_id": self.class_id,
            "class_name": self.class_name,
            "recurring": self.recurring,
            "credit_hours": self.credit_hours,
            "prereqs": self.prereqs,
            "requirement_designation": self.requirement_designation,
            "campus": self.campus,
            "class_desc": self.class_desc
        }

    @staticmethod
    def from_dict(data):
        """
        Convert a dictionary (e.g., from MongoDB) back into a ClassModel object.
        """
        return Class_Model(
            class_id=data.get("class_id"),
            class_name=data.get("class_name"),
            recurring=data.get("recurring"),
            credit_hours=data.get("credit_hours"),
            prereqs=data.get("prereqs", []),
            requirement_designation=data.get("requirement_designation", []),
            campus=data.get("campus"),
            class_desc=data.get("class_desc")
        )

    def __repr__(self):
        return (
            f"ClassModel(class_id={self.class_id}, "
            f"class_name='{self.class_name}', "
            f"recurring='{self.recurring}', "
            f"credit_hours={self.credit_hours}, "
            f"prereqs={self.prereqs}, "
            f"requirement_designation={self.requirement_designation}, "
            f"campus='{self.campus}', "
            f"class_desc='{self.class_desc}')"
        )
        
    def __str__(self):
        return f"{self.class_id}: ({self.credit_hours} credits)({self.recurring})"