import pandas as pd
import random
import json
import math
from pymongo import MongoClient
from tqdm import tqdm

print("Loading model...")
from sentence_transformers import SentenceTransformer, util
from torch import Tensor
from torch.cuda import is_available 
device = "cuda" if is_available() else "cpu"
model = SentenceTransformer('all-MiniLM-L6-v2').to(device)
print("Model loaded.")

all_requirements = ["First Year Seminar", "Humanities, Arts, Performance", "Humanities and Arts", "Natural Science", "Natural Sciences", "Quantitative Reasoning", "Mathematics and Quantitative Reasoning", "Social Science", "First Year Seminar", "First Year Writing", "Writing", "Continuing Communication", "Intercultural Communication", "Race and Ethnicity", "Experience and Application", "Physical Education", "Health"]

class Course:
    def __init__(self, course_id: str, section: int, crn: int, course_name: str, recurring: str, prereqs: list[str], requirement_designation: list[str], campus: str, description: str, professor: 'Professor', desc_vector=None):
        if not (course_id and section) and not crn: raise AmbiguousCourseError
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
        # TODO: Add meeting times, seats, location, capacity, permission req, credits attributes
    # TODO: Add is_full method, check_prereqs method 
    def __repr__(self):
        return json.dumps({
            "course_id": self.course_id,
            "section": self.section,
            "crn": self.crn,
            "course_name": self.course_name,
            "recurring": self.recurring,
            "prereqs": self.prereqs,
            "requirement_designation": self.requirement_designation,
            "campus": self.campus,
            "description": self.description,
            "professor": str({
            "name": self.professor.name,
            "email": self.professor.email,
            "rmp_rating": self.professor.rmp_rating
            })
        }, indent=4)


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
   def __init__(self, rmp_rating: str | float, ger: list[str], prereqs: str | list[str], campus: str, semester: str, description: str):
        if isinstance(rmp_rating, str): assert rmp_rating in ["high", None], "rmp_rating must be 'high' or None"
        else: assert 0 <= rmp_rating <= 5, "rmp_rating must be a float between 0 and 5"
        if not isinstance(prereqs, list): assert prereqs in ["high", "low", None], "prereqs must be 'high', 'low', or None or a list of prereqs"
        assert campus in ["Emory", "Oxford", None], "campus must be 'Emory', 'Oxford', or None"
        assert semester in ["fall", "spring", "summer", None], "recurring must be 'fall', 'spring', 'summer', or None"
        self.rmp_rating = rmp_rating # min rmp score or preference for high vs low score
        self.ger = ger
        self.prereqs = prereqs
        self.campus = campus
        self.semester = semester
        self.description = description
        
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
            desc_vector=course.get("desc_vector", None)
        )
        course_objs.append(course_obj)

    return course_objs


def calculate_suitability(course: Course, preferences: Preferences, return_details=False) -> float | dict:
    if not course:
        raise NullCourseError
    if not course.crn and not course.course_id and not course.section:
        raise AmbiguousCourseError

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

    if preferences.prereqs:
        if isinstance(preferences.prereqs, str):
            prereq_score = sum(len(req.split("or")) for req in course.prereqs) / len(course.prereqs) if course.prereqs else 0
            if preferences.prereqs == "low":
                prereq_score = 10 - prereq_score # inverse
            else:
                prereq_score = 0
            prereq_score /= 10
        elif not course.prereqs:
            prereq_score = 1
        else:
            prereq_score = 0
            for completed_req in preferences.prereqs:
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

    scores = [rmp_rating, ger_score, prereq_score, campus_score, description_score]
    preference_scores = [score for score in scores if score is not None]
    suitability_score = sum(preference_scores) / len(preference_scores) if preference_scores else 0
    
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

def main():
    print("Retrieving course data...")
    courses = data_loader(uri="mongodb://localhost:27017/", db_name="my_database", collection_name="Class")
    print("Course data retrieved.")

    preferences = Preferences(
        rmp_rating="high",
        ger=["Humanities and Arts", "Natural Science"],
        prereqs=["CS170", "CS171"],
        campus="Emory",
        semester="fall",
        description="I would like to learn about data structures and algorithms.",
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
        for score_obj in top_10:
            score_obj["suitability_score"] = incorporate_desc_similarity_scores(score_obj, preference_vector)
        top_10.sort(key=lambda x: x["suitability_score"], reverse=True)

    # Print the top 5 courses
    print("\nTop 5 Courses:")
    for score in top_10[:5]:
        course_name = score["course"].course_name
        suitability = score["suitability_score"]
        print(f"{course_name}: {suitability:.4f}")

if __name__ == "__main__":
    main()
