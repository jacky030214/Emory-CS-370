# class_detail.py

from Class_Model import Class_Model

class Class_Detail(Class_Model):
    def __init__(
        self,
        class_id,
        class_number,
        class_name,
        recurring,
        credit_hours,
        prereqs=None,
        requirement_designation=None,
        campus=None,
        class_desc=None,
        section=None,
        professor=None,
        time_slot=None,
        days=None,
        class_size=None,
        offering=None,
        room=None
    ):
        """
        Inherit from ClassModel, plus add details about a specific section.
        
        :param class_id: Inherited from ClassModel
        :param class_number: Inherited from ClassModel
        :param class_name: Inherited from ClassModel
        :param recurring: Inherited from ClassModel
        :param credit_hours: Inherited from ClassModel
        :param prereqs: Inherited from ClassModel
        :param requirement_designation: Inherited from ClassModel
        :param campus: Inherited from ClassModel
        :param class_desc: Inherited from ClassModel

        :param section: Specific section identifier (string or int)
        :param professor: Name of the instructor (string)
        :param time_slot: Time range (e.g., "09:00-09:50 AM")
        :param days: Days of the week (e.g., ["Mon", "Wed", "Fri"] or "MWF")
        :param class_size: The capacity for this section (int)
        :param offering: "virtual", "inperson", or "hybrid"
        :param room: The room number or location (string)
        """
        # Call the parent constructor first
        super().__init__(
            class_id=class_id,
            class_number=class_number,
            class_name=class_name,
            recurring=recurring,
            credit_hours=credit_hours,
            prereqs=prereqs,
            requirement_designation=requirement_designation,
            campus=campus,
            class_desc=class_desc
        )

        # Add subclass-specific attributes
        self.section = section
        self.professor = professor
        self.time_slot = time_slot
        self.days = days if days else []
        self.class_size = class_size
        self.offering = offering
        self.room = room

    def to_dict(self):
        """
        Extend the parent's dictionary representation with section-specific details.
        """
        base_dict = super().to_dict()
        base_dict.update({
            "section": self.section,
            "professor": self.professor,
            "time_slot": self.time_slot,
            "days": self.days,
            "class_size": self.class_size,
            "offering": self.offering,
            "room": self.room
        })
        return base_dict

    @staticmethod
    def from_dict(data):
        """
        Build a Class_Detail object from a dictionary, including both parent and child attributes.
        """
        # Create an instance by passing dictionary items to constructor
        return Class_Detail(
            class_id=data.get("class_id"),
            class_number=data.get("class_number"),
            class_name=data.get("class_name"),
            recurring=data.get("recurring"),
            credit_hours=data.get("credit_hours"),
            prereqs=data.get("prereqs", []),
            requirement_designation=data.get("requirement_designation", []),
            campus=data.get("campus"),
            class_desc=data.get("class_desc"),
            section=data.get("section"),
            professor=data.get("professor"),
            time_slot=data.get("time_slot"),
            days=data.get("days", []),
            class_size=data.get("class_size"),
            offering=data.get("offering"),
            room=data.get("room")
        )

    def __repr__(self):
        """
        Include both parent and child attributes in the string representation.
        """
        parent_repr = super().__repr__()
        return (
            f"{parent_repr[:-1]}, "
            f"section='{self.section}', "
            f"professor='{self.professor}', "
            f"time_slot='{self.time_slot}', "
            f"days={self.days}, "
            f"class_size={self.class_size}, "
            f"offering='{self.offering}', "
            f"room='{self.room}')"
        )
