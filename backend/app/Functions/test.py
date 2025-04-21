import os, sys
# Go up 3 levels from this file to get to the project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

import unittest
from unittest.mock import MagicMock
from backend.app.Functions.generate_personalized_schedule import get_top_k_courses, convert_to_Course_obj, Preferences, Course, Professor
from backend.app.Models.Class_Detail_Model import Class_Detail
from backend.app.Models.Class_Model import Class_Model
from backend.app.Models.Semester_Schedule_Model import Semester_Schedule
# Removed unused import for data_loader

class TestGeneratePersonalizedSchedule(unittest.TestCase):

    def setUp(self):
        # Mock Class_Detail and Class_Model objects
        self.mock_class_detail = Class_Detail(
            class_id="CS170",
            class_num=12345,
            class_name="Introduction to Computer Science",
            recurring="fall",
            credit_hours=3
        )
        self.mock_class_detail.prereqs = ["MATH111"]
        self.mock_class_detail.requirement_designation = ["Quantitative Reasoning"]
        self.mock_class_detail.campus = "EM"
        self.mock_class_detail.class_desc = "Learn the basics of computer science."
        self.mock_class_detail.section = 1
        self.mock_class_detail.class_num = 12345
        self.mock_class_detail.professor = Professor("Dr. Smith", "smith@university.edu", 4.5)
        self.mock_class_model = Class_Model(
            class_id="CS171",
            class_name="Data Structures",
            recurring="spring",
            credit_hours=3
        )
        self.mock_class_model.recurring = "spring"
        self.mock_class_model.credit_hours = 3
        self.mock_class_model.prereqs = ["CS170"]
        self.mock_class_model.requirement_designation = ["Quantitative Reasoning"]
        self.mock_class_model.campus = "EM"
        self.mock_class_model.class_desc = "Learn about data structures."
        self.mock_class_model.section = 2
        self.mock_class_model.class_num = 67890
        self.mock_class_model.professor = Professor("Dr. Johnson", "johnson@university.edu", 4.8)
        self.mock_class_model.time_slot = "TTh 1:00pm-2:15pm"

        # Mock Semester_Schedule
        self.mock_schedule = Semester_Schedule(year=2025, semester="fall")
        self.mock_schedule.classes = [self.mock_class_detail, self.mock_class_model]

    def test_convert_to_Course_obj(self):
        # Test conversion of Class_Detail to Course
        course_obj = convert_to_Course_obj(self.mock_class_detail)
        self.assertIsInstance(course_obj, Course)
        self.assertEqual(course_obj.course_id, "CS170")
        self.assertEqual(course_obj.course_name, "Introduction to Computer Science")
        self.assertEqual(course_obj.campus, "Emory")

        # Test conversion of Class_Model to Course
        course_obj = convert_to_Course_obj(self.mock_class_model)
        self.assertIsInstance(course_obj, Course)
        self.assertEqual(course_obj.course_id, "CS171")
        self.assertEqual(course_obj.course_name, "Data Structures")
        self.assertEqual(course_obj.campus, "Emory")

    def test_get_top_k_courses(self):
        # Mock preferences
        preferences = Preferences(
            rmp_rating="high",
            ger=["Quantitative Reasoning"],
            taken=["CS170"],
            campus="Emory",
            semester="fall",
            description="I want to learn about data structures and algorithms.",
            times=["MW 10:00am-11:15am", "TTh 1:00pm-2:15pm"]
        )

        # Mock data_loader to return a list of Course objects
        mock_course_1 = Course(
            course_id="CS170",
            section=1,
            crn=12345,
            course_name="Introduction to Computer Science",
            recurring="fall",
            taken=["MATH111"],
            requirement_designation=["Quantitative Reasoning"],
            campus="Emory",
            description="Learn the basics of computer science.",
            professor=Professor("Dr. Smith", "smith@university.edu", 4.5),
            time="MW 10:00am-11:15am"
        )

        mock_course_2 = Course(
            course_id="CS171",
            section=2,
            crn=67890,
            course_name="Data Structures",
            recurring="spring",
            taken=["CS170"],
            requirement_designation=["Quantitative Reasoning"],
            campus="Emory",
            description="Learn about data structures.",
            professor=Professor("Dr. Johnson", "johnson@university.edu", 4.8),
            time="TTh 1:00pm-2:15pm"
        )
        # Removed redefinition of data_loader
        mock_courses = [mock_course_1, mock_course_2]

        # Mock data_loader function
        data_loader = MagicMock(return_value=mock_courses)
        # Removed unused data_loader mock
        # Call get_top_k_courses
        top_k_courses = get_top_k_courses([self.mock_schedule], preferences, k=2)

        # Verify the results
        self.assertEqual(len(top_k_courses), 2)
        self.assertEqual(top_k_courses[0][0].course_id, "CS171")
        self.assertEqual(top_k_courses[1][0].course_id, "CS170")

if __name__ == "__main__":
    unittest.main()