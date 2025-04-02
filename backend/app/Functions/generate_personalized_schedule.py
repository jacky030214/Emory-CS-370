import pandas as pd
import random

all_requirements = ["Humanities and Arts", "Natural Science", "Quantitative Reasoning", "Social Science", "First Year Seminar", "First Year Writing", "Continuing Communication", "Intercultural Communication", "Race and Ethnicity", "Experience and Application", "Physical Education", "Health"]

class Course:
    def __init__(self, course_id: str, section: int, crn: int, course_name: str, recurring: str, prereqs: list[str], requirement_designation: list[str], campus: str, description: str, professor: 'Professor'):
        if not (course_id and section) and not crn: raise AmbiguousCourseError
        assert recurring in ["fall", "spring", "summer", "fall/spring", None], "recurring must be 'fall', 'spring', 'summer', 'fall/spring', or None"
        for req in requirement_designation:
            assert req in all_requirements, f"requirement_designation array values must be one of the following: {all_requirements}"
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
        # TODO: Add meeting times, seats, location, capacity, permission req, credits attributes
    # TODO: Add is_full method, check_prereqs method 

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
   def __init__(self, rmp_score: str | float, ger: list[str], prereqs: str | list[str], campus: str, semester: str, description: str):
        if isinstance(rmp_score, str): assert rmp_score in ["high", None], "rmp_score must be 'high' or None"
        else: assert 0 <= rmp_score <= 5, "rmp_score must be a float between 0 and 5"
        if not isinstance(prereqs, list): assert prereqs in ["high", "low", None], "prereqs must be 'high', 'low', or None or a list of prereqs"
        assert campus in ["Emory", "Oxford", None], "campus must be 'Emory', 'Oxford', or None"
        assert semester in ["fall", "spring", "summer", None], "recurring must be 'fall', 'spring', 'summer', or None"
        self.rmp_score = rmp_score # min rmp score or preference for high vs low score
        self.ger = ger
        self.prereqs = prereqs
        self.campus = campus
        self.semester = semester
        self.description = description
        
# TODO: Add semester selection to all functions 
AmbiguousCourseError = ValueError("Course object must have either (course_id and section) or crn.")
NullCourseError = ValueError("Course object cannot be null.")

def calculate_suitability(course: Course, preferences: Preferences, include_desc: bool = False) -> float:
    if not course:
        raise NullCourseError
    if not course.crn and not course.course_id and not course.section:
        raise AmbiguousCourseError

    RMP_score = course.professor.rmp_rating
    prereq_score = sum(len(req.split("or")) for req in course.prereqs) / len(course.prereqs) if course.prereqs else 0
    campus_score = 1 if course.campus == preferences.campus else 0
    
    if include_desc:
        if preferences.description:
            from sentence_transformers import SentenceTransformer, util
            model = SentenceTransformer('all-MiniLM-L6-v2')
            description_embeddings = model.encode(course.description, convert_to_tensor=True)
            preferred_desc_embeddings = model.encode(preferences.description, convert_to_tensor=True)
            similarities = util.pytorch_cos_sim(description_embeddings, preferred_desc_embeddings)
            description_score = float(similarities[0][0])
        else:
            description_score = 0

    # update scores based on preferences
    if isinstance(preferences.rmp_score, str):
        if preferences.rmp_score == "high":
            RMP_score *= 2
        else:
            RMP_score = 0
    elif preferences.rmp_score is not None:
        if RMP_score >= preferences.rmp_score:
            RMP_score *= 2
        else:
            RMP_score = 0
    
    GER_score = 0
    for ger in course.requirement_designation:
        if ger in preferences.ger:
            GER_score += 1

    # TODO: fix this heuristic to use completed prereqs
    if preferences.prereqs == "few":
        prereq_score = 10 - prereq_score # inverse
        if prereq_score < 0:
            prereq_score = 0 # if more than 10 prereqs then worst score
    else:
        prereq_score = 0
    
    if preferences.campus == course.campus:
        campus_score *= 2
    else:
        campus_score = 0

    # normalize individual attribute scores
    RMP_score /= 5
    GER_score /= len(preferences.ger) if preferences.ger else 0
    prereq_score /= 10
    campus_score /= 2
    description_score /= 1
    
    # TODO: fix final summation to not disregard zero scores and instead disregard None scores in final avg (also fix logic above)
    scores = [RMP_score, GER_score, prereq_score, campus_score, description_score]
    print(scores)
    non_zero_scores = [score for score in scores if score > 0]
    suitability_score = sum(non_zero_scores) / len(non_zero_scores) if non_zero_scores else 0
    return suitability_score

def main():
    preferences = Preferences(
        rmp_score="high",
        ger=["Humanities and Arts", "Natural Science"],
        prereqs=["CS170", "CS171"],
        campus="Emory",
        semester="fall",
        description="I would like to learn about data structures and algorithms.",
    )

    professor = Professor(name="Dr. Smith Wilson", email="smith_wilson@emory.edu", rmp_rating=4.5)

    good_course = Course(
        course_id="CS253",
        section=1,
        crn=None,
        course_name="0Data Structures and Algorithms",
        recurring="fall",
        prereqs=["CS171 or 171Z or CS_OX171"],
        requirement_designation=["Quantitative Reasoning", "Natural Science"],
        campus="Emory",
        description="A third course in Computer Science, focusing on advanced programming. Emphasis is on mastery in the use and implementation of data structures and algorithms for classical programming paradigms, using the Java programming language and object oriented design.",
        professor=professor,
    )

    bad_course = Course(
        course_id="CS224",
        section=1,
        crn=None,
        course_name="0Foundations of Computer Science",
        recurring="fall/spring",
        prereqs=["CS170 or CS_OX170", "MATH111 or MATH_OX111)"],
        requirement_designation=["Quantitative Reasoning"],
        campus="Oxford",
        description="An introductory course in the theory of Computer Science, focusing on analysis of discrete structures with applications. Emphasis is on developing familiarity with notation, computational acuity and creative problem solving skills.",
        professor=professor,
    )

    almost_good_course = Course(
        course_id="CS253",
        section=1,
        crn=None,
        course_name="1Data Structures and Algorithms",
        recurring="fall",
        prereqs=["CS171 or 171Z or CS_OX171"],
        requirement_designation=["Quantitative Reasoning"],
        campus="Emory",
        description="A third course in Computer Science, focusing on advanced programming. Emphasis is on mastery in the use and implementation of data structures and algorithms for classical programming paradigms, using the Java programming language and object oriented design.",
        professor=professor,
    )

    for course in [good_course, bad_course, almost_good_course]:
        suitability_score = calculate_suitability(course=course, preferences=preferences, include_desc=True)
        print(f"Suitability Score for {course.course_name}: {suitability_score}")

if __name__ == "__main__":
    main()
