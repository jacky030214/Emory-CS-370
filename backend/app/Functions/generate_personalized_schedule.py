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
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
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
print("Model loaded on:", device)

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
        assert recurring in ["fall", "spring", "summer", "fall/spring", "fall/spring/summer", None], f"recurring must be 'fall', 'spring', 'summer', 'fall/spring', 'fall/spring/summer', or None, not {recurring}"
        # for req in requirement_designation:
        #     assert req in all_requirements, f"requirement_designation array value: {req} must be one of the following: {all_requirements}"
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

class Preferences:
   def __init__(self, rmp_rating: str | float, ger: list[str], taken: str | list[str], campus: str, semester: str, description: str, times: list[str]):
        if isinstance(rmp_rating, str): assert rmp_rating in ["high", None], "rmp_rating must be 'high' or None"
        elif isinstance(rmp_rating, float) or isinstance(rmp_rating, int): assert 0 <= rmp_rating <= 5, "rmp_rating must be a float between 0 and 5"
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

def get_rmp_score(uri: str, db_name: str, collection_name: str, instructor_name: str) -> float:
    client = MongoClient(uri)
    db = client[db_name]
    collection = db[collection_name]
    result = collection.find_one({"name": instructor_name})
    return result.get("rating", 0) if result else 0


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
        if "campus" in course.keys():
            if course["campus"] == "EM":
                course["campus"] = "Emory"
            elif course["campus"] == "OX":
                course["campus"] = "Oxford"
        if "course_description" in course.keys():
            if "course_code" in course.keys():
                course["course_description"] = course["course_code"] + "\n" + course["course_description"]
            if "course_title" in course.keys():
                course["course_description"] = course["course_title"] + "\n" + course["course_description"]
        rmp_score = 0
        if "instructor_name" in course.keys():
            rmp_score = get_rmp_score(uri, db_name, collection_name, course["instructor_name"])
            
        course_obj = Course(
            course_id=course.get("course_code", "Failed To Retrieve"),
            section=course.get("course_section", 1),
            crn=course.get("course_crn", 0000),
            course_name=course.get("course_title", "Failed To Retrieve"),
            recurring=course.get("semesters_offered", "fall/spring"),
            prereqs=course.get("prerequisites", []),
            requirement_designation=course.get("requirement_designation", []),
            campus=course.get("campus", "Emory"),
            description=course.get("course_description", "Failed To Retrieve"),
            professor=Professor(
                name=course.get("instructor_name", "Failed To Retrieve"),
                email=course.get("instructor_email", "Failed To Retrieve"),
                rmp_rating=rmp_score
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
        campus_score = 1 if course.campus == preferences.campus else -10
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
    

def incorporate_desc_similarity_scores(score_details: dict, preference_vector: Tensor) -> dict:
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
        return 0
    if not hasattr(course, "desc_vector") or not course.desc_vector:
        score_details["description_score"] = 0
        score_details["suitability_score"] = score_details["suitability_score"] / 2
        return score_details
    if course.description == "undef" or "Failed To Retrieve" in course.description:
        score_details["description_score"] = 0
        score_details["suitability_score"] = score_details["suitability_score"] / 2
        return score_details
    
    course.desc_vector = Tensor(course.desc_vector).to(device)
    preference_vector = preference_vector.to(device)

    description_score = util.pytorch_cos_sim(course.desc_vector, preference_vector)
    description_score = float(description_score[0][0]) # extract score from tensor
    curr_score = score_details["suitability_score"]
    new_suitability_score = (curr_score + description_score*2) / 2
    score_details["suitability_score"] = new_suitability_score
    score_details["description_score"] = description_score
    return score_details


def generate_all_desc_vectors(uri: str, db_name: str, collection_name: str):
    """
    Generates all course description vectors and saves them to the database.
    """
    # connect to the database
    client = MongoClient(uri)
    db = client[db_name]
    collection = db[collection_name]

    # load all courses from the database
    courses = list(collection.find())

    # check if desc_vector already exists for 10 random courses
    random_courses = random.sample(courses, min(10, len(courses)))
    counter = 0
    for course in random_courses:
        if "desc_vector" in course.keys() and "course_description" in course.keys() and course["desc_vector"] is not None:
            counter += 1
        elif "course_description" not in course.keys():
            counter += 1
        if counter == 10:
            return

    # generate description vectors for each course
    for course in tqdm(courses, desc="Generating description vectors..."):
        course = dict(course)
        # add course_id and class_name to class_desc
        if "course_description" in course.keys():
            if "course_code" in course.keys():
                course["course_description"] = course["course_code"] + "\n" + course["course_description"]
            if "course_title" in course.keys():
                course["course_description"] = course["course_title"] + "\n" + course["course_description"]
            # generate and save the description vector
            desc_vector = model.encode(course["course_description"], convert_to_tensor=True)
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
    if isinstance(course, Class_Model) and hasattr(course, "class_id"):
        course_id = course.class_id
        course_name = course.class_name
        recurring = course.recurring
        prereqs = course.prereqs if course.prereqs else []
        requirement_designation = course.requirement_designation if course.requirement_designation else []
        campus = course.campus
        description = course.class_desc
        time = course.timeslot

        return Course(
            course_id=course_id,
            section=None,
            crn=None,
            course_name=course_name,
            recurring=recurring,
            prereqs=prereqs,
            requirement_designation=requirement_designation,
            campus= "Emory" if campus == "EM" else "Oxford",
            description=description,
            professor=None,
            time=time,
            desc_vector=model.encode(description, convert_to_tensor=True) if description else None
        )
    if isinstance(course, Class_Detail) and hasattr(course, "course_code"):
        course_id = course.course_code
        section = course.course_section
        crn = course.course_crn
        course_name = course.course_title
        recurring = course.semesters_offered
        prereqs = course.prerequisites if course.prerequisites else []
        requirement_designation = course.requirement_designation if course.requirement_designation else []
        campus = course.campus
        description = course.course_description
        professor = Professor(
            name=course.instructor_name,
            email=course.instructor_email,
            rmp_rating=0
        )
        time = course.meeting_time

    return Course(
        course_id=course_id,
        section=section,
        crn=crn,
        course_name=course_name,
        recurring=recurring,
        prereqs=prereqs,
        requirement_designation=requirement_designation,
        campus= "Emory" if campus == "EM" else "Oxford",
        description=description,
        professor=professor,
        time=time,
        desc_vector=model.encode(description, convert_to_tensor=True) if description else None
    )

def list_to_Course(data: dict) -> Course:
    if "campus" in data.keys():
        if data["campus"] == "EM":
            data["campus"] = "Emory"
        elif data["campus"] == "OX":
            data["campus"] = "Oxford"
    if "requirement_designation" in data.keys():
        if isinstance(data["requirement_designation"], str):
            data["requirement_designation"] = [data["requirement_designation"]]
    return Course (
        course_id = data.get("course_id", "undef"),
        section = data.get("section", 0),
        crn = data.get("crn", 0),
        course_name = data.get("course_name", "undef"),
        recurring = data.get("recurring", "undef"),
        prereqs = data.get("prereqs", []),
        requirement_designation = data.get("requirement_designation", []),
        campus = data.get("campus", "undef"),
        description = data.get("description", "undef"),
        professor = Professor(
            name=data.get("professor", {}).get("name", "undef"),
            email=data.get("professor", {}).get("email", "undef"),
            rmp_rating=data.get("professor", {}).get("rmp_rating", 0)
        ),
        time = data.get("time", "MWTThF 12:00am-1:00am"),
    )

def list_to_Preferences(data: dict) -> Preferences:
    rmp_rating = data.get("rmp_rating", None)
    ger = data.get("ger", [])
    taken = data.get("taken", [])
    campus = data.get("campus", None)
    semester = data.get("semester", None)
    description = data.get("description", None)
    times = data.get("times", None)

    return Preferences(
        rmp_rating=rmp_rating,
        ger=ger,
        taken=taken,
        campus=campus,
        semester=semester,
        description=description,
        times=times
    )

def get_top_k_courses(all_schedules: list[dict], preferences: dict, k: int = 5, undergraduate_only = True, collection_name="all_courses") -> list[dict]:
    taken_courses = []
    for semester in all_schedules:
        taken_courses.extend(semester.get("classes", []))
    
    taken_courses = [list_to_Course(course) for course in taken_courses]
    preferences = list_to_Preferences(preferences)

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

    print("Loading course data...")
    all_courses = data_loader(uri="mongodb://localhost:27017/", db_name="my_database", collection_name=collection_name)
    print("Course data loaded.")

    # Calculate suitability scores for all courses
    score_objs = []
    for course in all_courses:
        score_obj = calculate_suitability(course=course, preferences=preferences, return_details=True)
        score_objs.append(score_obj)
    
    # Get top 10 courses
    score_objs.sort(key=lambda x: x["suitability_score"], reverse=True)
    top_k = score_objs

    # Update suitability scores with description similarity scores if needed
    if preference_vector is not None:
        for i, score_obj in enumerate(top_k):
            top_k[i] = incorporate_desc_similarity_scores(score_obj, preference_vector)
        top_k.sort(key=lambda x: x["suitability_score"], reverse=True)
    # import json
    # with open("score_objs.json", "w") as json_file:
    #     json.dump(score_objs, json_file, default=lambda o: o.to_dict() if hasattr(o, "to_dict") else o, indent=4)

    if undergraduate_only:
        filtered_top_k = []
        for i, score_obj in enumerate(top_k):
            for char in score_obj["course"].course_id:
                if char.isdigit():
                    break
            if char.isdigit() and not int(char) >= 5:
                filtered_top_k.append(score_obj)
        top_k = filtered_top_k

    return top_k[:k]

def main():
    print("gen1")
    generate_all_desc_vectors(uri="mongodb://localhost:27017/", db_name="my_database", collection_name="all_courses")
    print("gen2")
    generate_all_desc_vectors(uri="mongodb://localhost:27017/", db_name="my_database", collection_name="fall_2025")
    print("gen3")
    generate_all_desc_vectors(uri="mongodb://localhost:27017/", db_name="my_database", collection_name="spring_2025")
    # FALL 2024
    all_schedules = [{"year":0,"semester":"Fall","classes":[{"class_id":"Math275","class_name":"Honors Linear Algebra","recurring":"fall","credit_hours":4,"prereqs":"AP Calculus BC","requirement_designation":[],"campus":"EM","class_desc":"This course is the first half of the advanced math introductory sequence. It covers the basics of linear algebra: vector spaces, linear transformations, determinants, and eigenvalues, with an emphasis on mathematical rigor. This class is for freshmen who scored a 5 on the Calculus AP BC exam.","timeslot":None},{"class_id":"Math111","class_name":"Calculus I","recurring":"fall/spring","credit_hours":3,"prereqs":[],"requirement_designation":"Quantitative Reasoning","campus":"EM","class_desc":"Limits, continuity, derivatives, antiderivatives, the definite integral.","timeslot":None}],"total_credit_hours":7},{"year":1,"semester":"Spring","classes":[{"class_id":"Math210","class_name":"Advanced Calculus for Data Sciences","recurring":"fall/spring","credit_hours":4,"prereqs":"Math111 or Math115 or Math119","requirement_designation":"Quantitative Reasoning","campus":"EM","class_desc":"This course is a short treatment of?MATH 112?and?211?with a lab component. It is not appropriate for students who have taken?MATH 211. Topics include: advanced integration, Taylor series; and multivariable differentiation, optimization and integration; and applications to statistics and science.","timeslot":None},{"class_id":"Math112","class_name":"Calculus II","recurring":"fall/spring","credit_hours":3,"prereqs":"Math111 or Math115 or Math119","requirement_designation":"Quantitative Reasoning","campus":"EM","class_desc":"Techniques of integration, exponential and logarithm functions, sequences and series, polar coordinates.","timeslot":None}],"total_credit_hours":7},{"year":1,"semester":"Fall","classes":[{"class_id":"Math211","class_name":"Advanced Calculus (Multivariable)","recurring":"fall/spring","credit_hours":3,"prereqs":"Math112","requirement_designation":"Quantitative Reasoning","campus":"EM","class_desc":"Vectors; multivariable functions; partial derivatives; multiple integrals; vector and scalar fields; Green's and Stokes' theorems; divergence theorem.","timeslot":None},{"class_id":"Math212","class_name":"Differential Equations","recurring":"fall/spring","credit_hours":3,"prereqs":"Math112","requirement_designation":"Quantitative Reasoning","campus":"EM","class_desc":"This is a standard first semester Differential Equations course which covers first and second-order differential equations and systems of differential equations, with an emphasis placed on developing techniques for solving differential equations.","timeslot":None},{"class_id":"Math221","class_name":"Linear Algebra","recurring":"fall/spring","credit_hours":4,"prereqs":"Math111 or Math112","requirement_designation":"Quantitative Reasoning","campus":"EM","class_desc":"Systems of linear equations, matrices, determinants, linear transformations, eigenvalues and eigenvectors, least-squares.","timeslot":None},{"class_id":"Math250","class_name":"Foundations of Mathematics","recurring":"fall/spring","credit_hours":3,"prereqs":"Math111; Math112","requirement_designation":"Quantitative Reasoning","campus":"EM","class_desc":"An introduction to theoretical mathematics. Logic and proofs, operations on sets, induction, relations, functions.","timeslot":None}],"total_credit_hours":13},{"year":2,"semester":"Spring","classes":[],"total_credit_hours":0},{"year":2,"semester":"Fall","classes":[],"total_credit_hours":0},{"year":3,"semester":"Spring","classes":[],"total_credit_hours":0},{"year":3,"semester":"Fall","classes":[],"total_credit_hours":0},{"year":4,"semester":"Spring","classes":[],"total_credit_hours":0}]

    topk = get_top_k_courses(all_schedules, Preferences(
        rmp_rating="high",
        ger=[],
        taken=["CS170", "CS171"],
        campus="Emory",
        semester="fall",
        description="I want to learn about data structures and algorithms using Java.",
        times = ["TTh 1:00pm-2:00pm"]
    ), k=5)

    from pprint import pprint
    for score_obj in topk:
        pprint(score_obj)
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
    score_objs = []
    for course in courses:
        score_obj = calculate_suitability(course=course, preferences=preferences, return_details=True)
        score_objs.append(score_obj)
    
    # Get top 10 courses
    score_objs.sort(key=lambda x: x["suitability_score"], reverse=True)
    top_10 = score_objs[:10]

    # Update suitability scores with description similarity scores if needed
    if preference_vector is not None:
        for i, score_obj in enumerate(top_10):
            top_10[i] = incorporate_desc_similarity_scores(score_obj, preference_vector)
        top_10.sort(key=lambda x: x["suitability_score"], reverse=True)

    # Print the top 5 courses
    print("\nTop 5 Courses:")
    for score in top_10[:5]:
        course_name = score["course"].course_name
        suitability = score["suitability_score"]
        print(f"{course_name}: {suitability:.4f}")

if __name__ == "__main__":
    main()
