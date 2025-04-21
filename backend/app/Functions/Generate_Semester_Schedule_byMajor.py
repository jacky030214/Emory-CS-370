import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pymongo import MongoClient
#from Models.Major_Req_Model import MajorRequirement  # Your MajorRequirement model with from_dict() method
from Models.Semester_Schedule_Model import Semester_Schedule  # Your simplified Semester_Schedule_Model class
from Models.Class_Model import Class_Model
from Models.Class_Detail_Model import Class_Detail
from Functions.Get_Major_Req_byName import get_major_requirements_by_name
from Functions.Get_Class_byID import get_class_by_id
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
                                if elective_id == 'MATH275' or elective_id == 'MATH276':
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
    for sem in schedule:
        
        semester_schedule_objects.append(Semester_Schedule(year = year, semester = "Fall" if isFall else "Spring", classes = sem ))
        if isFall:
            year += 1
            isFall = False
        else: isFall = True

    return semester_schedule_objects
        

def add_GER_course(schedule, isBulePlan = False, isEM = True, takenClass = None):
    """
    Add GER classes into exsiting schedule 
    
    :param schedule: List of semesters, where each semester is a list of class objects.
    :param isBluePlan: To identify if the student is taking Blue plan (default is False, taking Gold plan).
    :param isEM: To identify if the student is taking all courses in EM, False if if OX continuess.
    :return: List of semesters, where each semester is a list of class objects.
    """
    
    """
    EM Gold plan: 
    Area 1: First Year Seminar (first 2 semester, 1 course)
    Area 2: First Year Writing (first 2 semester, 1 course)
    Area 3: Continuing Writing (3 courses)
    Area 4: Math and Quantitative Reasoning (1 course)
    Area 5: Science, Nature, Technology (2 courses, 1 with lab)
    Area 6: History, Society, Cultures (2 courses)
    Area 7: Humanities, Arts, Language / Humanities, Arts, Performance (4 courses, 2 sequential courses in a single foreign language, 2 HAP or HAL (must 1 above 100 level for HAL) or 1 HAP 1 HAL)
    Area 8: Personal Health (1 one-hour course)
    Area 9: Physical Education and Dance (2 one-hour courses, one must be Principles of Physical Fitness course)
    Area 10: Race and Ethnicity (1 course, can be combined with other GER)
    
    """
    
    """
    EM Blue plan: 
    end of first year: ECS101, HLTH100, PE(PED) (1 course), First Year Seminar(FS)(1 course), First Year Writing(FW)(1 course)
    end of second year: Humanities and Arts(HA)(1 course), Natural Science(NS)(1 course), Quantitative Reasoning(QR)(1 course), Social Science(SS)(1 course)
    end of third year: Intercultural Communication(IC)(2 courses), Race and Ethnicity(ETHN)(1 course)
    end of college: Continuing Commnuication(CC)(2 courses), Experience and Application(XA)(1 course)
    """
    if (isBulePlan):
        # Connect to MongoDB
        uri="mongodb://localhost:27017/", 
        db_name="my_database"
        client = MongoClient(uri)
        db = client[db_name]
        classes_collection = db["Class"]
        
        
        # Create List for GER classes
        GER_class_obj = []
        GER_class_id = []
        allclasses_id = []
        allclasses_obj = []
        
        for sem in schedule:
            for cls in sem.classes:
                allclasses_id.append(cls.class_id)
                allclasses_obj.append(cls)
        
        

        
    else:
        # Connect to MongoDB
        uri="mongodb://localhost:27017/", 
        db_name="my_database"
        client = MongoClient(uri)
        db = client[db_name]
        classes_collection = db["Class"]
        
        
        # Create List for GER classes
        GER_class_obj = []
        GER_class_id = []
        allclasses_id = []
        allclasses_obj = []
        area1=1
        area2=1
        area3=3
        area4=1
        area5_1=1
        area5_2=1
        area6=2
        area7_1=2
        area7_2=2
        area8=1
        area9=2
        
        
        
        for sem in schedule:
            for cls in sem.classes:
                allclasses_id.append(cls.class_id)
                allclasses_obj.append(cls)
        for cls in takenClass:
            allclasses_id.append(cls)
        for cls in allclasses_obj:
            if  "First Year Seminar with Race Ethnicity" in cls.requirement_designation:
                area1 = area1-1
            elif "FirstYear Writing" in cls.requirement_designation:
                area2 = area2-1
            elif "writing" in cls.requirement_designation:
                area3 = area3-1
            elif "Quantitative Reasoning" in cls.requirement_designation:
                area4 = area4-1
            elif "lab" in cls.requirement_designation:
                area5_1 = area5_1-1
            elif "Science Nature" in cls.requirement_designation:
                area5_2 = area5_2-1
            elif "History Society Cultures" in cls.requirement_designation:
                area6 = area6-1
            elif "Intercultural Communication" in cls.requirement_designation:
                area7_1 = area7_1-1
            elif "Humanities Arts Performance" in cls.requirement_designation:
                area7_2 = area7_2-1
            elif "Physical Education" in cls.requirement_designation:
                area9 = area9-1
        
        # Area 1 and Area 10
        # Retrieve the document to find requirement_designation:
        doc = classes_collection.find({"requirement_designation": "First Year Seminar with Race  Ethnicity"})
        while(area1>0):
            cls_doc = next(doc)
            if cls_doc:
                # doc = next(doc, None)
                # Convert the document into a Course object using the model's from_dict method
                class_obj = Class_Model.from_dict(cls_doc)
                class_id = class_obj.class_id
                if class_id not in (allclasses_id and GER_class_id):
                    GER_class_obj.append(class_obj)
                    GER_class_id.append(class_id)
                    area1-=1    
                
        # Area 2
        # Retrieve the document to find requirement_designation:
        doc = classes_collection.find({"requirement_designation": "FirstYear Writing"})
        while(area2>0):
            cls_doc = next(doc)
            if cls_doc:
                # Convert the document into a Course object using the model's from_dict method
                class_obj = Class_Model.from_dict(cls_doc)
                class_id = class_obj.class_id
                if class_id not in (GER_class_id and allclasses_id):
                    GER_class_obj.append(class_obj)
                    GER_class_id.append(class_id)
                    area2-=1
                    
        # Area 3:
        doc = classes_collection.find({"requirement_designation": {"$regex": "writing", "$options": "i"}})
        while(area3>0):
            cls_doc=next(doc)
            if cls_doc:
                # Convert the document into a Course object using the model's from_dict method
                class_obj = Class_Model.from_dict(cls_doc)
                class_id = class_obj.class_id
                if class_obj.prereqs != []:
                    continue
                if class_id not in (GER_class_id and allclasses_id):
                    GER_class_obj.append(class_obj)
                    GER_class_id.append(class_id)
                    area3-=1
                 
        # Area 4:
        doc = classes_collection.find({"requirement_designation": {"$regex": "Quantitative Reasoning", "$options": "i"}})
        while(area4>0):
            cls_doc=next(doc)
            if cls_doc:
                # Convert the document into a Course object using the model's from_dict method
                class_obj = Class_Model.from_dict(cls_doc)
                class_id = class_obj.class_id
                if class_id not in (GER_class_id and allclasses_id):
                    GER_class_obj.append(class_obj)
                    GER_class_id.append(class_id)
                    area4-=1

                    
        # Area 5:

        doc = classes_collection.find({"requirement_designation": {"$regex": "lab", "$options": "i"}})
        while(area5_1):
            cls_doc = next(doc)
            if doc:
                # Convert the document into a Course object using the model's from_dict method
                class_obj = Class_Model.from_dict(cls_doc)
                class_id = class_obj.class_id
                if class_id not in (GER_class_id and allclasses_id):
                    GER_class_obj.append(class_obj)
                    GER_class_id.append(class_id)
                    area5_1-=1

        doc = classes_collection.find({"requirement_designation": {"$regex": "Science Nature", "$options": "i"}})
        while(area5_2):
            cls_doc = next(doc) 
            if cls_doc:
                # Convert the document into a Course object using the model's from_dict method
                class_obj = Class_Model.from_dict(cls_doc)
                class_id = class_obj.class_id
                if class_id not in (GER_class_id and allclasses_id):
                    GER_class_obj.append(class_obj)
                    GER_class_id.append(class_id)
                    area5_2-=1
                    
                    
        # Area 6:
        doc = classes_collection.find({"requirement_designation": {"$regex": "History Society Cultures", "$options": "i"}})
        while(area6>0):
            cls_doc = next(doc)
            if cls_doc:
                # Convert the document into a Course object using the model's from_dict method
                class_obj = Class_Model.from_dict(cls_doc)
                class_id = class_obj.class_id
                if class_id not in (GER_class_id and allclasses_id):
                    GER_class_obj.append(class_obj)
                    GER_class_id.append(class_id)
                    area6-=1
                    
                    
        # Area 7:
        doc = classes_collection.find({"requirement_designation": {"$regex": "Intercultural Communication", "$options": "i"}, "class_id": {"$regex": "ITAL", "$options": "i"}})
        while(area7_1>0):
            cls_doc = next(doc)
            if cls_doc:
                # Convert the document into a Course object using the model's from_dict method
                class_obj = Class_Model.from_dict(cls_doc)
                class_id = class_obj.class_id
                if class_id not in (GER_class_id and allclasses_id):
                    GER_class_obj.append(class_obj)
                    GER_class_id.append(class_id)
                    area7_1-=1
        doc = classes_collection.find({"requirement_designation": {"$regex": "Humanities Arts Performance", "$options": "i"}})
        while(area7_2>0):
            cls_doc = next(doc)
            if cls_doc:
                # Convert the document into a Course object using the model's from_dict method
                class_obj = Class_Model.from_dict(cls_doc)
                class_id = class_obj.class_id
                if class_id not in (GER_class_id and allclasses_id):
                    GER_class_obj.append(class_obj)
                    GER_class_id.append(class_id)
                    area7_2-=1
                    
                    
        # Area 9:
        doc = classes_collection.find({"requirement_designation": {"$regex": "Physical Education", "$options": "i"}})
        while(area9>0):
            cls_doc
            if cls_doc:
                # Convert the document into a Course object using the model's from_dict method
                class_obj = Class_Model.from_dict(cls_doc)
                class_id = class_obj.class_id
                if class_id not in (GER_class_id and allclasses_id):
                    GER_class_obj.append(class_obj)
                    GER_class_id.append(class_id)
                    area9-=1
                    
    # First, ensure that missing prerequisites are inserted.
    for ger_class in GER_class_obj:
        if ger_class.prereqs:
            groups = parse_prereq_string(ger_class.prereqs)
            for group in groups:
                # Check if any alternative from the group is already scheduled.
                if not any(is_course_in_schedule(schedule, candidate) for candidate in group):
                    # If missing, fetch and insert the first candidate.
                    candidate_course = get_class_by_id(group[0], uri, db_name)
                    if candidate_course:
                        if not insert_course_into_earliest_possible_semester(schedule, candidate_course, 19):
                            print(f"Warning: Could not insert missing prerequisite {candidate_course.class_id} for GER class {ger_class.class_id}")
                    else:
                        print(f"Warning: Prerequisite course {group[0]} not found for GER class {ger_class.class_id}")

    # Now, insert each GER class into the earliest semester where prerequisites are satisfied.
    for ger_class in GER_class_obj:
        inserted = False
        for sem_index in range(len(schedule)):
            if prerequisites_satisfied(ger_class, sem_index, schedule):
                if schedule[sem_index]._total_credit_hours + ger_class.credit_hours <= 19:
                    schedule[sem_index].add_class(ger_class)
                    print(f"Inserted GER class {ger_class.class_id} into semester {schedule[sem_index].semester} {schedule[sem_index].year}")
                    inserted = True
                    break
        if not inserted:
            print(f"Warning: Could not insert GER class {ger_class.class_id} due to credit or prerequisite constraints.")
    
        
    # for sem in schedule:
    #     while(sem._total_credit_hours <= 16 and len(GER_class_obj)!=0):
    #         sem.add_class(GER_class_obj[0])
    #         del GER_class_obj[0]
    
    return schedule
            
        
    
def parse_prereq_string(prereq_str):
    """
    Parse a prerequisites string that may include ";" and "or".
    ";" separates groups of prerequisites that are all required.
    Within each group, "or" separates alternatives (only one is needed).
    
    E.g., "CS101 or MATH101; PHYS101" becomes:
         [["CS101", "MATH101"], ["PHYS101"]]
    """
    groups = []
    for group in prereq_str.split(';'):
        group = group.strip()
        if group:
            if " or " in group:
                candidates = [p.strip() for p in group.split(" or ") if p.strip()]
                groups.append(candidates)
            else:
                groups.append([group])
    return groups

def is_course_in_schedule(schedule, course_id):
    """
    Returns True if a course with the given course_id is already present anywhere in the schedule.
    """
    for sem in schedule:
        for cls in sem.classes:
            if cls.class_id == course_id:
                return True
    return False

def insert_course_into_earliest_possible_semester(schedule, course, max_credits=16):
    """
    Inserts a course into the earliest semester that has enough credit capacity.
    Returns True if insertion is successful.
    """
    for sem in schedule:
        if sem._total_credit_hours + course.credit_hours <= max_credits:
            sem.add_class(course)
            print(f"Inserted course {course.class_id} into semester {sem.semester} {sem.year}")
            return True
    return False

def prerequisites_satisfied(ger_class, sem_index, schedule):
    """
    Checks whether the prerequisites for ger_class are satisfied in all semesters before sem_index.
    It uses parse_prereq_string to handle both ";" and "or" within the prerequisite string.
    """
    if not ger_class.prereqs:
        return True
    groups = parse_prereq_string(ger_class.prereqs)
    scheduled_ids = set()
    for i in range(sem_index):
        for cls in schedule[i].classes:
            scheduled_ids.add(cls.class_id)
    # For each group, at least one candidate must be scheduled.
    for group in groups:
        if not any(candidate in scheduled_ids for candidate in group):
            return False
    return True


def Generate_Schedule_withTime(takenClasses, major_name):
    uri="mongodb://localhost:27017/"
    db_name="my_database"
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
            if class_obj.class_id in takenClasses:
                continue
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
                                if elective_id == 'MATH275' or elective_id == 'MATH276':
                                    continue
                                if elective_id in takenClasses:
                                    break
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
        prereqs = getattr(cls_obj, "prereqs", [])
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
                    if not any(item in all_dict for item in alternatives):
                        for pre in alternatives:
                            pre_obj = get_class_by_id(pre, uri, db_name)
                            if pre_obj:
                                if pre_obj.class_id in takenClasses:
                                    break
                                all_dict[pre_obj.class_id] = pre_obj
                                add_missing_prereqs(pre_obj, all_dict)
                                break
                            else:
                                print(f"Warning: Prerequisite class {pre} not found in the database.")
                else:
                    pre = part
                    if pre not in (all_dict and takenClasses):
                        pre_obj = get_class_by_id(pre, uri, db_name)
                        if pre_obj:
                            all_dict[pre_obj.class_id] = pre_obj
                            add_missing_prereqs(pre_obj, all_dict)
                        else:
                            print(f"Warning: Prerequisite class {pre} not found in the database.")
                

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
    semester_credits = [0]
    result = None

    def prerequisites_satisfied(cls, candidate_sem):
        # All transitive prerequisites must be scheduled in a semester before candidate_sem.
        for pre in transitive_prereqs.get(cls.class_id, set()):
            if pre not in assignment or assignment[pre] >= candidate_sem:
                return False
        return True
    all_class_id = []
    for cls in all_classes:
        all_class_id.append(cls.class_id)

    min_credits = 0
    num_semesters = 8
    startingSemester = "Fall"
    semester_credits = [0] * num_semesters
    max_credits = 19
    
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
    schedule = convert_schedule_to_obj(schedule, startYear=0, startsFall=True)
    schedule_GER = add_GER_course(schedule = schedule, takenClass=takenClasses)
    all_classes_id = []
    for sem in schedule_GER:
        for cls in sem.classes:
            all_classes_id.append(cls.class_id)
            

        

    
    def prerequisites_satisfied(section):
        for pre in transitive_prereqs.get(section.course_code, set()):
            if pre not in takenClasses:
                return False
        return True
    
    def backtrack(i, current_schedule, current_credits):
        nonlocal best_schedule
        # If exact match, we return immediately.
        if current_credits == max_credits:
            best_schedule = current_schedule
            best_credits = current_credits
            return True  # perfect schedule found
        
        if i == len(all_classes_id):
            # End of list; update best if better.
            if current_credits > best_schedule._total_credit_hours:
                best_schedule = current_schedule
                best_credits = current_credits
            return False
        client = MongoClient(uri)
        db = client[db_name]
        classes_detail_collection = db["Class_Detail"]
        # Option 1: Try to add a section for course_ids[i]
        found_solution = False
        course_id = all_classes_id[i]
        all_section = []
        doc = list(classes_detail_collection.find({"course_code": course_id}))
        j=0
        while (j < len(doc)):
            sec_doc = doc[j]
            if(sec_doc):
                sec_obj = Class_Detail.from_dict(sec_doc)
                all_section.append(sec_obj)
                j+=1
            else:
                break
        for section in all_section:
            # Check if prerequisites are met.
            if not prerequisites_satisfied(section):
                continue
            # Check if adding this section would exceed max_credit_hours.
            if current_credits + section.credit_hours > max_credits:
                continue
            # Check for time conflicts with already scheduled sections.
            conflict = False
            for scheduled in current_schedule.classes:
                if section.meeting_time == scheduled.meeting_time:
                    conflict = True
                    break
            if conflict:
                continue
            # Try adding this section.
            current_schedule.classes.append(section)
            current_schedule._total_credit_hours += section.credit_hours
            if backtrack(i + 1, current_schedule, current_credits + section.credit_hours):
                return True  # exit early if perfect schedule found
            # Backtrack.
            popped = current_schedule.classes.pop()
            current_schedule._total_credit_hours -= popped.credit_hours

        # Option 2: Skip this course (if no section fits or if you want to allow a subset selection)
        if backtrack(i + 1, current_schedule, current_credits):
            return True
        
        return found_solution

    best_schedule = Semester_Schedule(year=0, semester="Fall", classes=[])
    best_credits = 0
    
    backtrack(0, best_schedule, 0)

    for cls in best_schedule.classes:
        all_classes_id.remove(cls.course_code)
    print(best_schedule)
    print(all_classes_id)
    return [best_schedule, all_classes_id]

def generate_future_schedule(major_name, num_semesters, takenClasses = None, futureClasses = None, min_credits=12, max_credits=19, startingSemester = "Fall"):
    uri="mongodb://localhost:27017/"
    db_name="my_database"
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
            if class_obj.class_id in takenClasses:
                continue
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
                                if elective_id == 'MATH275' or elective_id == 'MATH276':
                                    continue
                                if elective_id in takenClasses:
                                    break
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
    if futureClasses:
        for cls_id in futureClasses:
            cls = get_class_by_id(cls_id)
            if cls:          
                all_classes.append(get_class_by_id(cls))
            else: 
                print(f"Warning: Class {elective_obj} not found in the database.")
    for cls in (required_classes and elective_classes):
        if cls in all_classes: continue
        all_classes.append(cls)

    
        
    

    # --- Augment the class set with any missing prerequisites ---
    # We'll use a dictionary mapping class_id -> class_obj.
    all_classes_dict = {cls.class_id: cls for cls in all_classes}
    
    def add_missing_prereqs(cls_obj, all_dict):
        groups = []
        prereqs = getattr(cls_obj, "prereqs", [])
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
                    if not any(item in all_dict for item in alternatives):
                        for pre in alternatives:
                            pre_obj = get_class_by_id(pre, uri, db_name)
                            if pre_obj:
                                if pre_obj.class_id in takenClasses:
                                    break
                                all_dict[pre_obj.class_id] = pre_obj
                                add_missing_prereqs(pre_obj, all_dict)
                                break
                            else:
                                print(f"Warning: Prerequisite class {pre} not found in the database.")
                else:
                    pre = part
                    if pre not in (all_dict and takenClasses):
                        pre_obj = get_class_by_id(pre, uri, db_name)
                        if pre_obj:
                            all_dict[pre_obj.class_id] = pre_obj
                            add_missing_prereqs(pre_obj, all_dict)
                        else:
                            print(f"Warning: Prerequisite class {pre} not found in the database.")
                

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
    semester_credits = [0]
    result = None

    def prerequisites_satisfied(cls, candidate_sem):
        # All transitive prerequisites must be scheduled in a semester before candidate_sem.
        for pre in transitive_prereqs.get(cls.class_id, set()):
            if pre not in assignment or assignment[pre] >= candidate_sem:
                return False
        return True
    all_class_id = []
    for cls in all_classes:
        all_class_id.append(cls.class_id)

    min_credits = 0
    num_semesters = 8
    startingSemester = "Fall"
    semester_credits = [0] * num_semesters
    max_credits = 19
    
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
    schedule = convert_schedule_to_obj(schedule, startYear=0, startsFall=True)
    schedule_GER = add_GER_course(schedule = schedule, takenClass=takenClasses)
    
    all_classes_id = []
    for sem in schedule_GER:
        print(sem)
        for cls in sem.classes:
            all_classes_id.append(cls.class_id)
    

    
    
    
    

# Example usage:
if __name__ == "__main__":
    # Generate_Schedule_withTime(["QTM110","MATH111","MATH112","QTM150","QTM151"], "Bachelor of Science in Applied Mathematics and Statistics")
    generate_future_schedule(major_name="Bachelor of Science in Applied Mathematics and Statistics", num_semesters=7, takenClasses=["QTM110","MATH111","MATH112","QTM150","QTM151"])
    """
    major_input = "Bachelor of Science in Applied Mathematics and Statistics"
    full_schedule = generate_full_schedule(major_input, num_semesters=8, min_credits=0, max_credits=18)
    StartYear = 2022
    IsFall = True
    
    # if full_schedule:
    #     for sem in full_schedule:
    #         sem.insert(0,"aaa")
    #         print(sem)
            
            
    if full_schedule:
        print("Generated Full Schedule: ")
        print("Major:", major_input)
        # for i, sem in enumerate(full_schedule, start=1):
            
    #     #     # Print only the class IDs for clarity.
    #     #     print(f"Semester {i}: {[cls.class_id for cls in sem]}")
            
        semester_schedules = convert_schedule_to_obj(full_schedule, startYear=2025, startsFall=True)
        for sem in semester_schedules:
            print(sem)
            
        GER_schedule = add_GER_course(semester_schedules, isBulePlan=False, isEM=True)
        for sem in GER_schedule:
            print(sem)
    else:
        print("Failed to generate a full schedule.")
    """    
        
    # schedule = generate_dummy_semester_schedule(major_input, year=2025, semester="Fall", elective_count=1)
    # if schedule:
    #     # print("Generated Semester Schedule:")
    #     class_ids = [course.class_id for course in schedule.classes if hasattr(course, "class_id")]
    #     print("Generated Semester Schedule - Class IDs:", class_ids, "Total Credit Hours:", schedule.total_credit_hours)
    #     # print(schedule)
    # else:
    #     print("Failed to generate schedule.")
