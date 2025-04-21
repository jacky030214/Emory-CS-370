# class_detail.py

from Models.Class_Model import Class_Model

class Class_Detail(Class_Model):
    def __init__(
        self,
        course_code,
        course_section,         
        course_crn,
        course_title,
        credit_hours,
        grading_mode,
        instruction_method,
        semesters_offered,
        dates,
        course_description,
        instructor_email,
        instructor_name,
        meeting_time,
        meeting_location,
        final_exam,
        class_type,
        campus,
        prerequisites,
        requirement_designation

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

        # Add the new variable and subclass-specific attributes
        self.course_code = course_code
        self.course_section = course_section       
        self.course_crn = course_crn
        self.course_title = course_title
        self.credit_hours = int(credit_hours)
        self.grading_mode = grading_mode
        self.instruction_method = instruction_method
        self.semesters_offered = semesters_offered
        self.dates = dates
        self.course_description = course_description
        self.instructor_email = instructor_email
        self.instructor_name = instructor_name
        self.meeting_time = meeting_time
        self.meeting_location = meeting_location
        self.final_exam = final_exam
        self.class_type = class_type
        self.campus = campus
        self.prerequisites = prerequisites
        self.requirement_designation = requirement_designation

    def to_dict(self):
        """
        Extend the parent's dictionary representation with section-specific details.
        """
        return {
            "course_code": self.course_code,
            "course_section": self.course_section,         
            "course_crn": self.course_crn,
            "course_title": self.course_title,
            "credit_hours": self.credit_hours,
            "grading_mode": self.grading_mode,
            "instruction_method": self.instruction_method,
            "semesters_offered": self.semesters_offered,
            "dates": self.dates,
            "course_description": self.course_description,
            "instructor_email": self.instructor_email,
            "instructor_name": self.instructor_name,
            "meeting_time": self.meeting_time,
            "meeting_location": self.meeting_location,
            "final_exam": self.final_exam,
            "class_type": self.class_type,
            "campus": self.campus,
            "prerequisites": self.prerequisites,
            "requirement_designation": self.requirement_designation
        }

    @staticmethod
    def from_dict(data):
        """
        Build a Class_Detail object from a dictionary, including both parent and child attributes.
        """
        return Class_Detail(
            course_code = data.get("course_code"),
            course_section = data.get("course_section"),         
            course_crn = data.get("course_crn"),
            course_title = data.get("course_title"),
            credit_hours = data.get("credit_hours"),
            grading_mode = data.get("grading_mode"),
            instruction_method = data.get("instruction_method"),
            semesters_offered = data.get("semesters_offered"),
            dates = data.get("dates"),
            course_description = data.get("course_description"),
            instructor_email = data.get("instructor_email"),
            instructor_name = data.get("instructor_name"),
            meeting_time = data.get("meeting_time"),
            meeting_location = data.get("meeting_location"),
            final_exam = data.get("final_exam"),
            class_type = data.get("class_type"),
            campus = data.get("campus"),
            prerequisites = data.get("prerequisites"),
            requirement_designation = data.get("requirement_designation")
        )

    def __repr__(self):
        """
        Include both parent and child attributes in the string representation.
        """
        parent_repr = super().__repr__()
        return (
            f"course_code='{self.course_code}', "
            f"course_title='{self.course_title}', "
            f"course_section='{self.course_section}', "
            f"instructor_name='{self.instructor_name}', "
            f"meeting_time='{self.meeting_time}', "
        )

    def __str__(self):
            return f"{self.course_code}: ({self.credit_hours} credits)({self.meeting_time})({self.instructor_name})"