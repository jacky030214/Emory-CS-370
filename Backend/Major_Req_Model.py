class MajorRequirement:
    def __init__(self, major_name, required_classes=None, elective1=None, elective2=None ,elective3=None, elective4=None, elective5=None, elective6=None, total_credits_required=None):
        """
        Initialize a MajorRequirement object.

        :param major_name: The name of the major (string).
        :param required_classes: List of required course identifiers (list of strings/IDs).
        :param elective_classes: List of elective course identifiers or elective groups (list).
        :param total_credits_required: Total credit hours required for the major (int).
        """
        self.major_name = major_name
        self.required_classes = required_classes if required_classes is not None else []
        self.elective1 = elective1 if elective1 is not None else []
        self.elective2 = elective2 if elective2 is not None else []
        self.elective3 = elective3 if elective3 is not None else []
        self.elective4 = elective4 if elective4 is not None else []
        self.elective5 = elective5 if elective5 is not None else []
        self.elective6 = elective6 if elective6 is not None else []
        self.total_credits_required = total_credits_required
        
        

    def to_dict(self):
        """
        Convert the MajorRequirement object into a dictionary suitable for MongoDB insertion.
        """
        return {
            "major_name": self.major_name,
            "required_classes": self.required_classes,
            "elective1": self.elective1,
            "elective2": self.elective2,
            "elective3": self.elective3,
            "elective4": self.elective4,
            "elective5": self.elective5,
            "elective6": self.elective6,
            "total_credits_required": self.total_credits_required
        }

    @staticmethod
    def from_dict(data):
        """
        Create a MajorRequirement object from a dictionary.
        """
        return MajorRequirement(
            major_name=data.get("major_name"),
            required_classes=data.get("required_classes", []),
            elective1=data.get("elective1", []),
            elective2=data.get("elective2", []),
            elective3=data.get("elective3", []),
            elective4=data.get("elective4", []),
            elective5=data.get("elective5", []),
            elective6=data.get("elective6", []),
            # elective1=data.get("elective1", []),
            total_credits_required=data.get("total_credits_required")
        )

    def __repr__(self):
        return (
            f"MajorRequirement(major_name='{self.major_name}', "
            f"required_classes={self.required_classes}, "
            f"elective1={self.elective1}, "
            f"elective2={self.elective2}, "
            f"elective3={self.elective3}, "
            f"elective4={self.elective4}, "
            f"elective5={self.elective5}, "
            f"elective6={self.elective6}, "
            f"total_credits_required={self.total_credits_required})"
        )
        
        