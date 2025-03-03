# class_detail.py

from Backend.Backend.Models.Class_Model import Class_Model

class Class_Detail(Class_Model):
    def __init__(
        self,
        class_id,
        class_num,         # New variable for the class number
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
        Inherit from Class_Model, plus add details about a specific section.
        
        :param class_id: Inherited from Class_Model.
        :param class_num: The class number (e.g., "101").
        :param class_name: Inherited from Class_Model.
        :param recurring: Inherited from Class_Model.
        :param credit_hours: Inherited from Class_Model.
        :param prereqs: Inherited from Class_Model.
        :param requirement_designation: Inherited from Class_Model.
        :param campus: Inherited from Class_Model.
        :param class_desc: Inherited from Class_Model.
        
        :param section: Specific section identifier.
        :param professor: Name of the instructor.
        :param time_slot: Time range (e.g., "09:00-09:50 AM").
        :param days: Days of the week (e.g., ["Mon", "Wed", "Fri"]).
        :param class_size: Capacity for this section.
        :param offering: "virtual", "inperson", or "hybrid".
        :param room: Room number or location.
        """
        # Call the parent constructor
        super().__init__(
            class_id=class_id,
            class_name=class_name,
            recurring=recurring,
            credit_hours=credit_hours,
            prereqs=prereqs,
            requirement_designation=requirement_designation,
            campus=campus,
            class_desc=class_desc
        )

        # Add the new variable and subclass-specific attributes
        self.class_num = class_num
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
            "class_num": self.class_num,
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
        return Class_Detail(
            class_id=data.get("class_id"),
            class_num=data.get("class_num"),
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
            f"class_num='{self.class_num}', "
            f"section='{self.section}', "
            f"professor='{self.professor}', "
            f"time_slot='{self.time_slot}', "
            f"days={self.days}, "
            f"class_size={self.class_size}, "
            f"offering='{self.offering}', "
            f"room='{self.room}')"
        )
