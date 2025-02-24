from Semester_Schedule_Model import Semester_Schedule

class Semester_Schedule_Detail(Semester_Schedule):
    def __init__(
        self,
        year,
        semester,
        monday=None,
        tuesday=None,
        wednesday=None,
        thursday=None,
        friday=None
    ):
        """
        :param year: Integer or string representing the year (e.g., 2025).
        :param semester: "Fall" or "Spring".
        :param monday: List of classes scheduled on Monday.
        :param tuesday: List of classes scheduled on Tuesday.
        :param wednesday: List of classes scheduled on Wednesday.
        :param thursday: List of classes scheduled on Thursday.
        :param friday: List of classes scheduled on Friday.
        """
        super().__init__(year, semester, classes=[])
        self.monday = monday if monday is not None else []
        self.tuesday = tuesday if tuesday is not None else []
        self.wednesday = wednesday if wednesday is not None else []
        self.thursday = thursday if thursday is not None else []
        self.friday = friday if friday is not None else []

    def to_dict(self):
        """
        Convert the Semester_Schedule object into a dictionary.
        Useful for inserting into databases like MongoDB.
        """
        return {
            "year": self.year,
            "semester": self.semester,
            "monday": self.monday,
            "tuesday": self.tuesday,
            "wednesday": self.wednesday,
            "thursday": self.thursday,
            "friday": self.friday
        }

    @staticmethod
    def from_dict(data):
        """
        Convert a dictionary to a Semester_Schedule object.
        Useful for retrieving from MongoDB and creating a Python object.
        """
        return Semester_Schedule_Detail(
            year=data.get("year"),
            semester=data.get("semester"),
            monday=data.get("monday", []),
            tuesday=data.get("tuesday", []),
            wednesday=data.get("wednesday", []),
            thursday=data.get("thursday", []),
            friday=data.get("friday", [])
        )

    def __repr__(self):
        return (
            f"Semester_Schedule_Detail(year={self.year}, semester='{self.semester}', "
            f"monday={self.monday}, tuesday={self.tuesday}, "
            f"wednesday={self.wednesday}, thursday={self.thursday}, friday={self.friday})"
        
        )