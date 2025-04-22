"""
Incorporate preference algo to elective decision in jacky algo (make special function that takes in a list of possible electives to choose from)
Add time conflict management in preference algo
Add two functionalities to preference algo - return k classes based on needed credit hours for full time status (15 minimum or 12 minimum) (GIVEN TIME CONTRAINT = T/F) AND return top 10 courses based on taken courses as suggestion AND given user preferences return top 10 courses
"""

import pandas as pd
import random
import json
import math
from pymongo import MongoClient
from tqdm import tqdm

import os, sys
# Go up 3 levels from this file to get to the project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from backend.app.Models.Class_Detail_Model import Class_Detail
from backend.app.Models.Class_Model import Class_Model
from backend.app.Models.Semester_Schedule_Model import Semester_Schedule

print("Loading model...")
from sentence_transformers import SentenceTransformer, util
from torch import Tensor
from torch.cuda import is_available as cuda_available
from torch.mps import is_available as mps_available
device = "cuda" if cuda_available() else "cpu"
device = "mps" if device == "cpu" and mps_available() else device
model = SentenceTransformer('all-MiniLM-L6-v2').to(device)
print("Model loaded.")

all_requirements = ["First Year Seminar", "Humanities, Arts, Performance", "Humanities and Arts", "Natural Science", "Natural Sciences", "Quantitative Reasoning", "Mathematics and Quantitative Reasoning", "Social Science", "First Year Seminar", "First Year Writing", "Writing", "Continuing Communication", "Intercultural Communication", "Race and Ethnicity", "Experience and Application", "Physical Education", "Health"]

def convert_to_24_hour(time_str):
        time_str = time_str.lower().replace(":", "") # 9:00am -> 900am or 2:00pm -> 200pm
        if "am" in time_str:
            time_str = time_str.replace("am", "")
            time_num = int(time_str)
            if time_num == 1200:  # handle 12:00am as 0
                return 0
            return time_num
        else:
            time_str = time_str.replace("pm", "")
            time_num = int(time_str)
            if time_num < 1200:  # add 12 hours for pm times except 12:XXpm
                return time_num + 1200
            return time_num

def parse_course_time(course_time: str) -> tuple[list[str], str, str]:
    course_time = course_time.split(" ")
    course_days_str = course_time[0]
    course_days = []
    if course_days_str.__contains__("M"):
        course_days.append("M")
        course_days_str = course_days_str.replace("M", "")
    if course_days_str.__contains__("W"):
        course_days.append("W")
        course_days_str = course_days_str.replace("W", "")
    if course_days_str.__contains__("Th"):
        course_days.append("Th")
        course_days_str = course_days_str.replace("Th", "")
    if course_days_str.__contains__("T"):
        course_days.append("T")
        course_days_str = course_days_str.replace("T", "")
    if course_days_str.__contains__("F"):
        course_days.append("F")
        course_days_str = course_days_str.replace("F", "")
    
    course_hours = course_time[1].split("-")
    course_start = course_hours[0]
    if not course_start.__contains__(":"):
        if course_start.__contains__("am"):
            course_start = course_start.replace("am", ":00am")
        else:
            course_start = course_start.replace("pm", ":00pm")
    course_end = course_hours[1]
    if not course_end.__contains__(":"):
        if course_end.__contains__("am"):
            course_end = course_end.replace("am", ":00am")
        else:
            course_end = course_end.replace("pm", ":00pm")

    course_start = convert_to_24_hour(course_start)
    course_end = convert_to_24_hour(course_end)
    return course_days, course_start, course_end

class Course:
    def __init__(self, course_id: str, section: int, crn: int, course_name: str, recurring: str, prereqs: list[str], requirement_designation: list[str], campus: str, description: str, professor: 'Professor', time: str = None, desc_vector=None):
        assert recurring in ["fall", "spring", "summer", "fall/spring", None], "recurring must be 'fall', 'spring', 'summer', 'fall/spring', or None"
        for req in requirement_designation:
            assert req in all_requirements, f"requirement_designation array value: {req} must be one of the following: {all_requirements}"
        assert campus in ["Emory", "Oxford", None], "campus must be 'Emory', 'Oxford', or None"
        self.course_id = course_id
        self.section = section
        self.crn = crn
        self.course_name = course_name
        self.recurring = recurring
        self.prereqs = prereqs
        self.requirement_designation = requirement_designation
        self.campus = campus
        self.description = description
        self.professor = professor
        if desc_vector is not None:
            self.desc_vector = desc_vector
        self.time = parse_course_time(time) if time else None
        # TODO: Add meeting times, seats, location, capacity, permission req, credits attributes
    # TODO: Add is_full method, check_prereqs method 
    def to_dict(self):
        return {
            "course_id": self.course_id if self.course_id is not None else "undef",
            "section": self.section if self.section is not None else "undef",
            "crn": self.crn if self.crn is not None else "undef",
            "course_name": self.course_name if self.course_name is not None else "undef",
            "recurring": self.recurring if self.recurring is not None else "undef",
            "prereqs": self.prereqs if self.prereqs is not None else "undef",
            "requirement_designation": self.requirement_designation if self.requirement_designation is not None else "undef",
            "campus": self.campus if self.campus is not None else "undef",
            "description": self.description if self.description is not None else "undef",
            "time": self.time if self.time is not None else "undef",
            "professor": {
                "name": self.professor.name if self.professor.name is not None else "undef",
                "email": self.professor.email if self.professor.email is not None else "undef",
                "rmp_rating": self.professor.rmp_rating if self.professor.rmp_rating is not None else "undef"
            } if self.professor is not None else "undef",
        }

    def __repr__(self):
        return json.dumps(self.to_dict(), indent=4)

class Professor:
    def __init__(self, name: str, email, rmp_rating: float):
        assert 0 <= rmp_rating <= 5, "rmp_rating must be between 0 and 5"
        self.name = name
        self.email = email
        self.rmp_rating = rmp_rating

class Schedule:
    def __init__(self, mon: list[Course], tues: list[Course], wed: list[Course], thurs: list[Course], fri: list[Course]):
        self.mon = mon
        self.tues = tues
        self.wed = wed
        self.thurs = thurs
        self.fri = fri

class Major:
    def __init__(self, name: str, requirements: dict[str, list[str]]):
        self.name = name
        self.requirements = requirements
        assert requirements.keys().__contains__("required_courses") and requirements.keys().__contains__("elective1"), "Major must have required_courses and at least a elective1 requirement"

class Preferences:
   def __init__(self, rmp_rating: str | float, ger: list[str], taken: str | list[str], campus: str, semester: str, description: str, times: list[str]):
        if isinstance(rmp_rating, str): assert rmp_rating in ["high", None], "rmp_rating must be 'high' or None"
        else: assert 0 <= rmp_rating <= 5, "rmp_rating must be a float between 0 and 5"
        if not isinstance(taken, list): assert taken in ["high", "low", None], "taken must be 'high', 'low', or None or a list of taken"
        assert campus in ["Emory", "Oxford", None], "campus must be 'Emory', 'Oxford', or None"
        assert semester in ["fall", "spring", "summer", None], "recurring must be 'fall', 'spring', 'summer', or None"
        self.rmp_rating = rmp_rating # min rmp score or preference for high vs low score
        self.ger = ger
        self.taken = taken
        self.campus = campus
        self.semester = semester
        self.description = description
        if times:
            self.times = []
            for time in times:
                self.times.append(parse_course_time(time))
        else:
            self.times = None

# TODO: Add semester selection to all functions 
AmbiguousCourseError = ValueError("Course object must have either (course_id and section) or crn.")
NullCourseError = ValueError("Course object cannot be null.")
NullPreferenceVectorError = ValueError("Preference vector cannot be null.")

def data_loader(uri: str, db_name: str, collection_name: str) -> list[Course]:
    """
    Loads data from a MongoDB collection into a pandas DataFrame.
    
    :param uri: MongoDB connection URI.
    :param db_name: Name of the database.
    :param collection_name: Name of the collection to load data from.
    :return: DataFrame containing the data from the specified collection.
    """
    client = MongoClient(uri)
    db = client[db_name]
    collection = db[collection_name]
    
    courses = list(collection.find())
    course_objs = []
    for course in courses:
        course = dict(course)
        if "requirement_designation" in course.keys():
            course["requirement_designation"] = course["requirement_designation"].split(" with ")
        if course["campus"] == "EM":
            course["campus"] = "Emory"
        elif course["campus"] == "OX":
            course["campus"] = "Oxford"
        if "class_desc" in course.keys():
            if "class_id" in course.keys():
                course["class_desc"] = course["class_id"] + "\n" + course["class_desc"]
            if "class_name" in course.keys():
                course["class_desc"] = course["class_name"] + "\n" + course["class_desc"]
        if "desc_vector" in course.keys():
            course["desc_vector"] = Tensor(course["desc_vector"]).to(device)
            
        course_obj = Course(
            course_id=course.get("class_id", "Failed To Retrieve"),
            section=course.get("section", 1),
            crn=course.get("crn", 0000),
            course_name=course.get("class_name", "Failed To Retrieve"),
            recurring=course.get("recurring", "fall/spring"),
            prereqs=course.get("prereqs", []),
            requirement_designation=course.get("requirement_designation", []),
            campus=course.get("campus", "Emory"),
            description=course.get("class_desc", "Failed To Retrieve"),
            professor=Professor(
                name=course.get("professor_name", "Failed To Retrieve"),
                email=course.get("email", "Failed To Retrieve"),
                rmp_rating=course.get("rmp_rating", 0)
            ),
            desc_vector=course.get("desc_vector", None),
            time=course.get("time", None)
        )
        course_objs.append(course_obj)

    return course_objs


def calculate_suitability(course: Course, preferences: Preferences, return_details=False) -> float | dict:
    if not course:
        raise NullCourseError
    if not course.crn and not course.course_id and not course.section:
        raise AmbiguousCourseError

    time_conflict = 0
    if check_time_conflict(course, preferences):
        time_conflict = 1       

    if preferences.rmp_rating:
        rmp_rating = course.professor.rmp_rating
        if isinstance(preferences.rmp_rating, str):
            if preferences.rmp_rating == "high":
                rmp_rating /= 5
            elif preferences.rmp_rating == "low":
                rmp_rating = 1 - (rmp_rating / 5)
        else:
            if rmp_rating >= preferences.rmp_rating:
                rmp_rating = 1 / (1 + math.exp(-5 * (course.professor.rmp_rating - preferences.rmp_rating))) # sigmoid based heuristic with k=5
    else:
        rmp_rating = None

    if preferences.taken:
        if isinstance(preferences.taken, str):
            prereq_score = sum(len(req.split("or")) for req in course.prereqs) / len(course.prereqs) if course.prereqs else 0
            if preferences.taken == "low":
                prereq_score = 10 - prereq_score # inverse
            else:
                prereq_score = 0
            prereq_score /= 10
        elif not course.prereqs:
            prereq_score = 1
        else:
            prereq_score = 0
            for completed_req in preferences.taken:
                for course_req in course.prereqs:
                    course_req = [req.strip() for req in course_req.split("or")]
                    if completed_req in course_req:
                        prereq_score += 1
                        break # move on to next completed_req
            prereq_score /= len(course.prereqs)
    else:
        prereq_score = None

    if preferences.campus:
        campus_score = 1 if course.campus == preferences.campus else 0
    else:
        campus_score = None
        
    if preferences.ger:
        ger_score = 0
        for ger in course.requirement_designation:
            if ger in preferences.ger:
                ger_score += 1
        ger_score /= len(preferences.ger)
    else:
        ger_score = None

    scores = [rmp_rating, ger_score, prereq_score, campus_score]
    preference_scores = [score for score in scores if score is not None]
    suitability_score = sum(preference_scores) / len(preference_scores) if preference_scores else 0
    suitability_score = suitability_score - time_conflict

    if not return_details:
        return suitability_score

    if return_details:
        return {
            "course": course,
            "suitability_score": suitability_score,
            "rmp_rating": rmp_rating,
            "ger_score": ger_score,
            "prereq_score": prereq_score,
            "campus_score": campus_score,
            "time_conflict": time_conflict
        }
    

def incorporate_desc_similarity_scores(score_details: dict, preference_vector: Tensor) -> float:
    """
    Calculates a new suitability score by incorporating the description similarity score.
    This function takes the current suitability score and combines it with a 
    description similarity score. The score_details dictionary must be one given by the
    `calculate_suitability()` function.

    :param score_details: A dictionary containing the course object and scores.
    :param preference_vector: User's preference description embeddings as a Tensor.

    :raises NullCourseError: If the "course" key is missing or None in `score_details`.
    :raises NullPreferenceVectorError: If `preference_vector` is None.
    
    :return: The updated suitability score as a float.
    """
    course = score_details.get("course", None)
    if not course:
        raise NullCourseError
    if preference_vector is None:
        raise NullPreferenceVectorError

    description_score = util.pytorch_cos_sim(course.desc_vector, preference_vector)
    description_score = float(description_score[0][0]) # extract score from tensor
    curr_score = score_details["suitability_score"]
    new_suitability_score = (curr_score + description_score) / 2

    return new_suitability_score


def generate_all_desc_vectors():
    """
    Generates all course description vectors and saves them to the database.
    """
    # connect to our database
    client = MongoClient("mongodb://localhost:27017/")
    db = client["my_database"]
    collection = db["Class"]

    # load all courses from the database
    courses = list(collection.find())

    # generate description vectors for each course
    for course in tqdm(courses, desc="Generating description vectors..."):
        course = dict(course)
        # add course_id and class_name to class_desc
        if "class_desc" in course.keys():
            if "class_id" in course.keys():
                course["class_desc"] = course["class_id"] + "\n" + course["class_desc"]
            if "class_name" in course.keys():
                course["class_desc"] = course["class_name"] + "\n" + course["class_desc"]
            # generate and save the description vector
            desc_vector = model.encode(course["class_desc"], convert_to_tensor=True)
            collection.update_one({"_id": course["_id"]}, {"$set": {"desc_vector": desc_vector.tolist()}})



def check_time_conflict(course: Course, preferences: Preferences) -> bool:
    if not course.time or not preferences.times:
        return False
    course_days, course_start, course_end = course.time
    preferences_times = preferences.times

    days_to_check = []
    for pref_time in preferences_times:
        pref_days, pref_start, pref_end = pref_time
        for course_day in course_days:
            if course_day in pref_days:
                if course_start < pref_end and pref_start < course_end:
                    return True
    return False

def convert_to_Course_obj(course: Class_Detail | Class_Model) -> Course:
    course_id = course.class_id
    course_name = course.class_name
    recurring = course.recurring
    credit_hours = course.credit_hours
    prereqs = course.prereqs
    requirement_designation = course.requirement_designation
    campus = "Oxford" if course.campus == "OX" else "Emory" if course.campus == "EM" else None
    description = course.class_desc

    # Use defaults for missing fields if Class_Model (i.e., base class)
    section = getattr(course, "section", 0)
    crn = getattr(course, "class_num", 0)
    professor = getattr(course, "professor", None)
    time = getattr(course, "time_slot", None)

    return Course(
        course_id=course_id,
        section=section,
        crn=crn,
        course_name=course_name,
        recurring=recurring,
        prereqs=prereqs,
        requirement_designation=requirement_designation,
        campus=campus,
        description=description,
        professor=professor,
        time=time
    )


def get_top_k_courses(all_schedules: list[Semester_Schedule], preferences: Preferences, k: int = 5) -> list[dict]:
    taken_courses = []
    for schedule in all_schedules:
        for course in schedule.classes:
            if isinstance(course, Class_Detail) or isinstance(course, Class_Model):
                taken_courses.append(convert_to_Course_obj(course))
    if hasattr(preferences, "taken") and isinstance(preferences.taken, list):
        for course in taken_courses:
            preferences.taken.append(course.course_id)
    else:
        preferences.taken = [course.course_id for course in taken_courses]

    desc = ""
    for course in taken_courses:
        desc += course.course_name + "\n"
        desc += course.description + "\n"
    if hasattr(course, "course_name") and hasattr(course, "description") and hasattr(preferences, "description"):
            desc = preferences.description + "\n" + desc
    preferences.description = desc
    
    preference_vector = model.encode(preferences.description, convert_to_tensor=True)

    courses = data_loader(uri="mongodb://localhost:27017/", db_name="my_database", collection_name="Class")

    # Calculate suitability scores for all courses
    courses_and_scores = []
    for course in courses:
        score_obj = calculate_suitability(course=course, preferences=preferences, return_details=True)
        courses_and_scores.append((course, score_obj))
    
    # Get top 10 courses
    courses_and_scores.sort(key=lambda x: x[1]["suitability_score"], reverse=True)
    top_k = courses_and_scores[:k]

    # Update suitability scores with description similarity scores if needed
    if preference_vector is not None:
        for i, (course, score_obj) in enumerate(top_k):
            score_obj["suitability_score"] = incorporate_desc_similarity_scores(score_obj, preference_vector)
            top_k[i] = (course, score_obj)  # Update the tuple with the modified score_obj
        top_k.sort(key=lambda x: x[1]["suitability_score"], reverse=True)


    return top_k

def main():
    # FALL 2024
    fall_classes = [
        Class_Detail(
            class_id="MATH101",
            class_num=1001,
            class_name="Calculus I",
            recurring="fall/spring",
            credit_hours=4,
            prereqs=[],
            requirement_designation=["Writing"],
            campus="EM",
            class_desc="Intro to derivatives and integrals.",
            section=1,
            professor=Professor("Dr. Newton", "newt@emory.edu", 4),
            time_slot="MW 1pm-2:15pm",
            days=["Mon", "Wed"],
            class_size=30,
            offering="inperson",
            room="MSC 101"
        ),
        Class_Model(  # Base class with fewer details
            class_id="ENG101",
            class_name="English Composition",
            recurring="fall/spring",
            credit_hours=3,
            prereqs=[],
            requirement_designation=["Writing"],
            campus="OX",
            class_desc="Develops skills in argumentative writing."
        )
    ]

    # SPRING 2025
    spring_classes = [
        Class_Detail(
            class_id="MATH102",
            class_num=1002,
            class_name="Calculus II",
            recurring="spring",
            credit_hours=4,
            prereqs=["MATH101"],
            requirement_designation=["Writing"],
            campus="EM",
            class_desc="Continuation of Calculus I.",
            section=1,
            professor=Professor("Dr. Leibniz", "lei@emory.edu", 5),
            time_slot="TTh 1pm-2:15pm",
            days=["Tue", "Thu"],
            class_size=30,
            offering="inperson",
            room="MSC 102"
        ),
        Class_Detail(
            class_id="CS170",
            class_num=1701,
            class_name="Intro to CS",
            recurring="spring",
            credit_hours=3,
            prereqs=[],
            requirement_designation=["Writing"],
            campus="EM",
            class_desc="Introduction to computer science fundamentals.",
            section=1,
            professor=Professor("Dr. Ada", "newt@emory.edu", 4),
            time_slot="MW 1pm-2:15pm",
            days=["Mon", "Wed"],
            class_size=40,
            offering="inperson",
            room="CSB 100"
        )
    ]

    # Wrap in Semester_Schedule
    semesters = [
        Semester_Schedule(year=2024, semester="Fall", classes=fall_classes),
        Semester_Schedule(year=2025, semester="Spring", classes=spring_classes)
    ]

    topk = get_top_k_courses(semesters, Preferences(
        rmp_rating="high",
        ger=["Humanities and Arts", "Natural Science"],
        taken=["CS170", "CS171"],
        campus="Emory",
        semester="fall",
        description="I would like to learn about data structures and algorithms.",
        times = ["TTh 11:30am-12:45pm", "F 1pm-2:15pm", "MW 8:30am-9:45am"]
    ), k=5)

    for course, score_obj in topk:
        print(course.to_dict())
        print(score_obj["suitability_score"])
        print()
        print()


    exit()
    print("Retrieving course data...")
    courses = data_loader(uri="mongodb://localhost:27017/", db_name="my_database", collection_name="Class")
    print("Course data retrieved.")

    preferences = Preferences(
        rmp_rating="high",
        ger=["Humanities and Arts", "Natural Science"],
        taken=["CS170", "CS171"],
        campus="Emory",
        semester="fall",
        description="I would like to learn about data structures and algorithms.",
        times = ["TTh 11:30am-12:45pm", "F 1pm-2:15pm", "MW 8:30am-9:45am"]
    )
    preference_vector = model.encode(preferences.description, convert_to_tensor=True) if preferences.description else None
    
    # Calculate suitability scores for all courses
    courses_and_scores = []
    for course in courses:
        score_obj = calculate_suitability(course=course, preferences=preferences, return_details=True)
        courses_and_scores.append((course, score_obj))
    
    # Get top 10 courses
    courses_and_scores.sort(key=lambda x: x[1]["suitability_score"], reverse=True)
    top_10 = courses_and_scores[:10]

    # Update suitability scores with description similarity scores if needed
    if preference_vector is not None:
        for i, (course, score_obj) in enumerate(top_10):
            score_obj["suitability_score"] = incorporate_desc_similarity_scores(score_obj, preference_vector)
            top_10[i] = (course, score_obj)  # Update the tuple with the modified score_obj
        top_10.sort(key=lambda x: x[1]["suitability_score"], reverse=True)

    # Print the top 5 courses
    print("\nTop 5 Courses:")
    for score in top_10[:5]:
        course_name = score[1]["course"].course_name
        suitability = score[1]["suitability_score"]
        print(f"{course_name}: {suitability:.4f}")

if __name__ == "__main__":
    main()
