from pymongo import MongoClient
from Class_Model import Class_Model

def get_class_by_id(class_id, uri="mongodb://localhost:27017/", db_name="my_database"):
    """
    Connects to MongoDB, retrieves a course document based on course_id,
    and returns it as a Course object.

    :param course_id: The identifier of the course (e.g., "Math111")
    :param uri: MongoDB connection URI (default is local instance)
    :param db_name: The name of the database containing the courses collection
    :return: A Course object if found, or None otherwise.
    """
    # Connect to MongoDB
    client = MongoClient(uri)
    db = client[db_name]
    
    # Assume that the collection is called "courses"
    classes_collection = db["Class"]
    
    # Retrieve the document where "course_id" matches the given course_id
    doc = classes_collection.find_one({"class_id": class_id})
    
    # Close the MongoDB connection
    client.close()
    
    if doc:
        # Convert the document into a Course object using the model's from_dict method
        return Class_Model.from_dict(doc)
    else:
        return None

# Example usage:
if __name__ == "__main__":
    # Let's try to fetch the course "Math111"
    course = get_class_by_id("Math111")
    if course:
        print("Retrieved Course Object:")
        print(course)
    else:
        print("Course not found.")