import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pymongo import MongoClient
from Models.Major_Req_Model import MajorRequirement
from pprint import pprint
import re

def get_major_requirements_by_name_aa(major_name, uri="mongodb://localhost:27017/", db_name="my_database"):
    """
    Retrieves the major requirements document from MongoDB based on the provided major name.
    
    :param major_name: Name of the major to search for.
    :param uri: MongoDB connection URI (default is localhost).
    :param db_name: Name of the database where major requirements are stored.
    :return: A MajorRequirement object if found, otherwise None.
    """
    # Connect to MongoDB
    client = MongoClient(uri)
    db = client[db_name]
    
    # Access the collection that stores major requirements
    major_req_collection = db["Major_Req"]
    
    # for doc in major_req_collection.find():
    #     pprint(doc)
    
    # Find the document matching the major name (case sensitive; adjust query if needed)
    doc = major_req_collection.find_one({"major_name": major_name})
    
    # Close the client connection
    client.close()
    
    if doc:
        # Process 'required_classes': if it's a string, split into a list.
        if "required_classes" in doc and isinstance(doc["required_classes"], str):
            raw_courses = [course.strip() for course in doc["required_classes"].split(';') if course.strip()]
            processed_courses = []
            for course in raw_courses:
                # If the course contains an " or ", split it into alternatives.
                if " or " in course:
                    alternatives = [alt.strip() for alt in course.split(" or ") if alt.strip()]
                    processed_courses.append(alternatives)
                else:
                    processed_courses.append(course)
            doc["required_classes"] = processed_courses

        # Combine elective fields (e.g., elective1, elective2, etc.) into one list.
        electives = []
        for key in doc:
            if key.startswith("elective"):
                value = doc[key].strip() if isinstance(doc[key], str) else ""
                if value:
                    electives.append(value)
        # Store the combined electives in the 'elective_courses' field
        doc["elective_courses"] = electives

        # Optionally, remove individual elective keys from the doc
        for i in range(1, 7):
            key = f"elective{i}"
            if key in doc:
                del doc[key]

        # Return the MajorRequirement object built from the processed document
        return MajorRequirement.from_dict(doc)
    else:
        return None
    
def get_major_requirements_by_name(major_name, uri="mongodb://localhost:27017/", db_name="my_database"):
    """
    Retrieves the major requirements document from MongoDB based on the provided major name.
    If a required (or elective) class is specified as "Math200*", it is replaced by a list of all 
    Math courses (from the Class_Model collection) whose numeric part is >= 200.
    
    :param major_name: Name of the major to search for.
    :param uri: MongoDB connection URI (default is localhost).
    :param db_name: Name of the database where major requirements are stored.
    :return: A MajorRequirement object if found, otherwise None.
    """
    client = MongoClient(uri)
    db = client[db_name]
    
    # Access the collection that stores major requirements.
    major_req_collection = db["Major_Req"]
    doc = major_req_collection.find_one({"major_name": major_name})
    
    if doc:
        # Process 'required_classes': if it's a string, split into a list.
        if "required_classes" in doc and isinstance(doc["required_classes"], str):
            raw_courses = [course.strip() for course in doc["required_classes"].split(';') if course.strip()]
            processed_courses = []
            for course in raw_courses:
                # If the course contains an " or ", split it into alternatives.
                if " or " in course:
                    alternatives = [alt.strip() for alt in course.split(" or ") if alt.strip()]
                    processed_courses.append(alternatives)
                else:
                    processed_courses.append(course)
            doc["required_classes"] = processed_courses

        # Combine elective fields (e.g., elective1, elective2, etc.) into one list.
        for key in doc:
            if key.startswith("elective"):
                processed_electives = []
                value = doc[key].strip() if isinstance(doc[key], str) else ""
                if value:
                    if value == "Math200*":
                        classes_collection = db["Class"]
                        regex = re.compile(r'^Math(\d+)$', re.IGNORECASE)
                        matching = []
                        for class_doc in classes_collection.find({"class_id": regex}):
                            m = regex.match(class_doc["class_id"])
                            if m and int(m.group(1)) >= 200:
                                matching.append(class_doc["class_id"])
                        if matching:
                            processed_electives.append(matching)
                        else:
                            processed_electives.append(value)
                    elif value == "Math300*":
                        classes_collection = db["Class"]
                        regex = re.compile(r'^Math(\d+)$', re.IGNORECASE)
                        matching = []
                        for class_doc in classes_collection.find({"class_id": regex}):
                            m = regex.match(class_doc["class_id"])
                            if m and int(m.group(1)) >= 300:
                                matching.append(class_doc["class_id"])
                        if matching:
                            processed_electives.append(matching)
                        else:
                            processed_electives.append(value)
                    elif value == "Math400*":
                        classes_collection = db["Class"]
                        regex = re.compile(r'^Math(\d+)$', re.IGNORECASE)
                        matching = []
                        for class_doc in classes_collection.find({"class_id": regex}):
                            m = regex.match(class_doc["class_id"])
                            if m and int(m.group(1)) >= 400:
                                matching.append(class_doc["class_id"])
                        if matching:
                            processed_electives.append(matching)
                        else:
                            processed_electives.append(value)        
                    elif " or " in value:
                        alternatives = [alt.strip() for alt in value.split(" or ") if alt.strip()]
                        processed_electives.append(alternatives)
                    elif ';' in value:
                        raw_courses = [course.strip() for course in value.split(';') if course.strip()]
                        processed_electives.append(raw_courses)
                    else:
                        processed_electives.append(value)
                    
                # print(processed_electives)
                doc[key] = processed_electives


        # Remove individual elective keys.

        
        client.close()
        return MajorRequirement.from_dict(doc)
    else:
        client.close()
        return None

# Example usage:
if __name__ == "__main__":
    major_name = "Bachelor of Science in Applied Mathematics Test"
    major_req = get_major_requirements_by_name(major_name)
    
    if major_req:
        print("Major Requirements for", major_name)
        print(major_req)
    else:
        print("No requirements found for", major_name)
