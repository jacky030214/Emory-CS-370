class Semester_Schedule:
    def __init__(self, year, semester, classes=None):
        """
        Initializes a schedule for one semester with a list of classes.

        :param year: e.g., 2025
        :param semester: "Fall" or "Spring"
        :param classes: A list of class objects (e.g., Class_Detail objects)
        """
        self.year = year
        self.semester = semester
        self.classes = classes if classes is not None else []
        self._total_credit_hours = sum(getattr(cls, 'credit_hours', 0) for cls in self.classes)

        
    @property
    def total_credit_hours(self):
        """
        Calculates the total credit hours by summing the credit_hours of all classes in the schedule.
        """
        return self._total_credit_hours

    def add_class(self, class_obj):
        """
        Adds a class object to the schedule.
        
        :param class_obj: A class object with a 'credit_hours' attribute.
        """
        self.classes.append(class_obj)
        self._total_credit_hours += getattr(class_obj, 'credit_hours', 0)

    def to_dict(self):
        """
        Convert the Semester_Schedule object into a dictionary for storage in MongoDB.
        If a class has a to_dict() method, it will be used.
        """
        return {
            "year": self.year,
            "semester": self.semester,
            "classes": [c.to_dict() if hasattr(c, "to_dict") else c for c in self.classes],
            "total_credit_hours": self.total_credit_hours
        }

    @staticmethod
    def from_dict(data):
        """
        Reconstruct a Semester_Schedule object from a dictionary.
        Note: You may need to convert the class dictionaries back to objects if desired.
        """
        classes = data.get("classes", [])
        return Semester_Schedule(
            year=data.get("year"),
            semester=data.get("semester"),
            classes=classes  # Optionally convert these to objects, e.g., Class_Detail.from_dict(item)
        )

    def __repr__(self):
        return (
            f"Semester_Schedule(year={self.year}, semester='{self.semester}', "
            f"classes={self.classes}, total_credit_hours={self.total_credit_hours})"
        )
        
    def __str__(self):
        classes_str = "\n    ".join(str(cls) for cls in self.classes)
        return f"{self.year}{self.semester}({self.total_credit_hours}):\n    {classes_str}"
        

