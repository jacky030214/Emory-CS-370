from pymongo import MongoClient
from Major_Req_Model import MajorRequirement  # Your MajorRequirement model with from_dict() method
from Semester_Schedule_Model import Semester_Schedule  # Your simplified Semester_Schedule_Model class
from Class_Model import Class_Model
from Get_Major_Req_byName import get_major_requirements_by_name
from Get_Class_byID import get_class_by_id
from pprint import pprint

def generate_dummy_semester_schedule(major_name, year=2025, semester="Fall", elective_count=1,
                               uri="mongodb://localhost:27017/", db_name="my_database"):
    """
    Generates a semester schedule for the given major. It retrieves the major requirements,
    then for each required course (and electives), it fetches the corresponding Course object
    and adds it to the schedule.
    
    If a required course is given as alternatives (e.g., ["CS170", "Math170"]),
    it picks the first alternative.
    
    :param major_name: Name of the major (string)
    :param year: Academic year (e.g., 2025)
    :param semester: Semester (e.g., "Fall" or "Spring")
    :param elective_count: Number of elective courses to add from the major requirements.
    :param uri: MongoDB connection URI.
    :param db_name: Name of the MongoDB database.
    :return: A Semester_Schedule object, or None if major requirements are not found.
    """
    # Retrieve the major requirements object.
    major_req = get_major_requirements_by_name(major_name, uri, db_name)
    if not major_req:
        print(f"Major requirements not found for {major_name}")
        return None

    schedule_classes = []
    print(major_req)
    
    print(major_req.required_classes)

    # Process each required course.
    for required in major_req.required_classes:
        if isinstance(required, list):
            # If alternatives exist, choose the first one.
            class_id = required[0]
        else:
            class_id = required

        class_obj = get_class_by_id(class_id, uri, db_name)
        if class_obj:
            schedule_classes.append(class_obj)
        else:
            print(f"Warning: Course {class_id} not found in the database.")

    # Optionally, add elective courses (if any) up to elective_count.
    elective_added = 0
    for elective in major_req.elective_classes:
        if elective_added >= elective_count:
            break
        class_obj = get_class_by_id(elective, uri, db_name)
        if class_obj:
            schedule_classes.append(class_obj)
            elective_added += 1
        else:
            print(f"Warning: Elective course {elective} not found in the database.")

    # Create a Semester_Schedule object with the list of courses.
    schedule = Semester_Schedule(year=year, semester=semester, classes=schedule_classes)
    return schedule




def generate_full_schedule(major_name, num_semesters, min_credits=12, max_credits=19,
                            uri="mongodb://localhost:27017/", db_name="my_database", startingSemester = "Fall"):
    """
    Generates a full multi-semester schedule that satisfies the major requirements, including electives.
    
    It retrieves the major requirements, collects the required classes (for any alternatives, picks the first option)
    and also selects a specified number of elective classes, then uses a backtracking algorithm to assign each class 
    a semester (from 1 to num_semesters) such that:
      - Each class is scheduled after all its prerequisites.
      - The total credit hours in each semester are between min_credits and max_credits.
    
    :param major_name: Name of the major (string).
    :param num_semesters: Total number of semesters (e.g., 8).
    :param min_credits: Minimum credits per semester.
    :param max_credits: Maximum credits per semester.
    :param elective_count: Number of elective classes to include from the major requirements.
    :param uri: MongoDB connection URI.
    :param db_name: MongoDB database name.
    :return: A list of lists, where each sublist corresponds to a semester’s scheduled classes, or None if no schedule found.
    """
    # Retrieve major requirements.
    major_req = get_major_requirements_by_name(major_name, uri, db_name)
    if not major_req:
        print(f"Major requirements not found for {major_name}")
        return None

    # Build list of required class objects.
    required_classes_id = []
    required_classes = []
    for class_item in major_req.required_classes:
        # If alternatives are provided, choose the first alternative.
        if isinstance(class_item, list):
            class_id = class_item[0]
        else:
            class_id = class_item

        class_obj = get_class_by_id(class_id, uri, db_name)
        if class_obj:
            required_classes.append(class_obj)
            required_classes_id.append(class_id)
        else:
            print(f"Warning: Class {class_id} not found in the database.")

    # Build list of elective class objects.
    # Choose first elective class from the list
    elective_classes_id = []
    for key in major_req.to_dict():
        if key.startswith("elective"):
            for elective_field in getattr(major_req, key):
                for elective in elective_field:
                    if isinstance(elective, list):
                        elective_id = elective[0]
                    else:
                        elective_id = elective
                    if get_class_by_id(elective_id, uri, db_name):
                        if elective_id not in elective_classes_id:
                            if elective_id not in required_classes_id:
                                if elective_id == 'Math275' or elective_id == 'Math276':
                                    continue
                                elective_classes_id.append(elective_id)
                                break
                    else:
                        print(f"Warning: Elective class {elective} not found in the database.")
                    
    elective_classes = []
    for elective_id in elective_classes_id:
        elective_obj = get_class_by_id(elective_id, uri, db_name)
        if elective_obj:
            elective_classes.append(elective_obj)
        else:
            print(f"Warning: Class {elective_obj} not found in the database.")
    
    
    # Combine required and elective classes.
    all_classes = []
    all_classes = required_classes + elective_classes
    

    # --- Augment the class set with any missing prerequisites ---
    # We'll use a dictionary mapping class_id -> class_obj.
    all_classes_dict = {cls.class_id: cls for cls in all_classes}
    
    def add_missing_prereqs(cls_obj, all_dict):
        groups = []
        prereqs = getattr(cls, "prereqs", [])
        if isinstance(prereqs, str):
            prereqs = [prereqs]
        for group_str in prereqs:
            # Now group_str is the full string, not a single character.
            if ";" in group_str:
                parts = [p.strip() for p in group_str.split(";") if p.strip()]
            else:
                parts = [group_str.strip()]
            for part in parts:
                if " or " in part:
                    alternatives = [p.strip() for p in part.split(" or ") if p.strip()]
                    if not any(item in all_dict for item in alternatives) :
                        pre = alternatives[0]
                        pre_obj = get_class_by_id(pre, uri, db_name)
                        if pre_obj:
                            all_dict[pre_obj.class_id] = pre_obj
                            add_missing_prereqs(pre_obj, all_dict)
                        else:
                            print(f"Warning: Prerequisite class {pre} not found in the database.")
                else:
                    pre = part
                    if pre not in all_dict:
                        pre_obj = get_class_by_id(pre, uri, db_name)
                        if pre_obj:
                            all_dict[pre_obj.class_id] = pre_obj
                            add_missing_prereqs(pre_obj, all_dict)
                        else:
                            print(f"Warning: Prerequisite class {pre} not found in the database.")
                

                
                    
                    
        # for pre in getattr(cls_obj, "prereqs", []):
        #     # Process prerequisite: if it contains " or ", choose the first alternative.
        #     if " or " in pre:
        #         pre = pre.split(" or ")[0].strip()
        #     else:
        #         pre = pre.strip()
        #     if pre and pre not in all_dict:
        #         pre_obj = get_class_by_id(pre, uri, db_name)
        #         if pre_obj:
        #             all_dict[pre_obj.class_id] = pre_obj
        #             add_missing_prereqs(pre_obj, all_dict)
        #         else:
        #             print(f"Warning: Prerequisite class {pre} not found in the database.")

    for cls in list(all_classes_dict.values()):
        add_missing_prereqs(cls, all_classes_dict)
    # Rebuild our full list.
    all_classes = list(all_classes_dict.values())
                    



    # Build a mapping from class_id to class object.
    class_dict = {cls.class_id: cls for cls in all_classes}
    
    # Build prerequisite groups.
    # For each class, assume cls.prereqs is a list of strings like:
    # ["Math210 or Math211", "Math221", "CS170 or Math170"]
    direct_prereqs = {}
    for cls in all_classes:
        direct = set()
        prereqs = getattr(cls, "prereqs", [])
        # Ensure prereqs is a list (if it's a string, make it a single-element list)
        if isinstance(prereqs, str):
            prereqs = [prereqs]
        for group_str in prereqs:
            # Now group_str is the full string, not a single character.
            if ";" in group_str:
                parts = [p.strip() for p in group_str.split(";") if p.strip()]
            else:
                parts = [group_str.strip()]
            for part in parts:
                if " or " in part:
                    candidate = [p.strip() for p in part.split(" or ") if p.strip()]
                    for item in candidate:
                        if item in class_dict:
                            direct.add(item)
                else:
                    candidate = part
                    if candidate in class_dict:
                        direct.add(candidate)
        direct_prereqs[cls.class_id] = direct
        
        
    # --- Compute transitive prerequisites using DFS ---
    memo = {}
    def compute_transitive(cid):
        if cid in memo:
            return memo[cid]
        trans = set(direct_prereqs.get(cid, []))
        for pre in direct_prereqs.get(cid, []):
            trans |= compute_transitive(pre)
        memo[cid] = trans
        return trans

    transitive_prereqs = {cid: compute_transitive(cid) for cid in class_dict}
        
        
    # Sort classes by number of prerequisite groups (fewer groups first)
    sorted_classes = sorted(all_classes, key=lambda cls: len(transitive_prereqs.get(cls.class_id, [])))
    
    # Backtracking algorithm.
    assignment = {}  # Mapping: class_id -> semester (1-indexed)
    semester_credits = [0] * num_semesters
    result = None

    def prerequisites_satisfied(cls, candidate_sem):
        # All transitive prerequisites must be scheduled in a semester before candidate_sem.
        for pre in transitive_prereqs.get(cls.class_id, set()):
            if pre not in assignment or assignment[pre] >= candidate_sem:
                return False
        return True

    def backtrack(i):
        nonlocal result
        if i == len(sorted_classes):
            if all(semester_credits[s] >= min_credits for s in range(num_semesters)):
                result = assignment.copy()
                return True
            return False
        
        cls = sorted_classes[i]
        if startingSemester == "Fall":
            isFall = True
        else:
            isFall = False
        # cls_rec = get_class_by_id(cls.class_id, uri, db_name).recurring
        for sem in range(1, num_semesters + 1):
            if not prerequisites_satisfied(cls, sem):
                isFall = not isFall
                continue
            if semester_credits[sem - 1] + cls.credit_hours > max_credits:
                isFall = not isFall
                continue
            if (cls.recurring == "fall" ) and not isFall:
                isFall = not isFall
                continue
            if (cls.recurring == "spring" ) and isFall:
                isFall = not isFall
                continue            
            assignment[cls.class_id] = sem
            semester_credits[sem - 1] += cls.credit_hours
            if backtrack(i + 1):
                return True
            del assignment[cls.class_id]
            semester_credits[sem - 1] -= cls.credit_hours
        return False

    if not backtrack(0):
        print("No valid schedule found!")
        return None

    # Build final schedule: list of semesters (each a list of class objects)
    schedule = [[] for _ in range(num_semesters)]
    for cls in sorted_classes:
        sem = result[cls.class_id]
        schedule[sem - 1].append(cls)
    return schedule

def convert_schedule_to_obj(schedule, startYear, startsFall):
    """
    Converts a schedule (list of lists of class objects) into a list of Semester_Schedule objects.
    
    :param schedule: List of semesters, where each semester is a list of class objects.
    :param StartYear: The starting academic year (e.g., 2025).
    :param startSem: The starting academeic semester (Fall/Spring).
    :return: List of Semester_Schedule objects.
    """
    # if len(schedule) != len(semester_labels):
    #     raise ValueError("Number of semesters in schedule must match the number of semester labels provided.")
    
    semester_schedule_objects = []
    semester_Count = len(schedule)
    year = startYear
    isFall = startsFall
    for sem in full_schedule:
        
        semester_schedule_objects.append(Semester_Schedule(year = year, semester = "Fall" if isFall else "Spring", classes = sem ))
        if isFall:
            year += 1
            isFall = False
        else: isFall = True

    return semester_schedule_objects
        


    

# Example usage:
if __name__ == "__main__":
    
    
        
    major_input = "Bachelor of Arts in Mathematics"
    full_schedule = generate_full_schedule(major_input, num_semesters=8, min_credits=0, max_credits=18)
    StartYear = 2022
    IsFall = True
    if full_schedule:
        print("Generated Full Schedule: ")
        print("Major:", major_input)
        # for i, sem in enumerate(full_schedule, start=1):
            
        #     # Print only the class IDs for clarity.
        #     print(f"Semester {i}: {[cls.class_id for cls in sem]}")
            
        semester_schedules = convert_schedule_to_obj(full_schedule, startYear=2025, startsFall=True)
        for sem in semester_schedules:
            print(sem)
    else:
        print("Failed to generate a full schedule.")
        
    # schedule = generate_dummy_semester_schedule(major_input, year=2025, semester="Fall", elective_count=1)
    # if schedule:
    #     # print("Generated Semester Schedule:")
    #     class_ids = [course.class_id for course in schedule.classes if hasattr(course, "class_id")]
    #     print("Generated Semester Schedule - Class IDs:", class_ids, "Total Credit Hours:", schedule.total_credit_hours)
    #     # print(schedule)
    # else:
    #     print("Failed to generate schedule.")
