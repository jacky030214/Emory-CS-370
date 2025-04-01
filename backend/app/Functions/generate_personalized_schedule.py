import pandas as pd

# TODO: Add semester selection to all functions 
CourseArgumentError = ValueError("You must provide either (course_id and section) or crn.")
PreferencesError = ValueError("You must provide student preferences.")

# rmp = rate my professor
def rmp_rating(course_id=None, section=None, crn=None):
    ratings = pd.read_csv("backend/app/Data/rmp_ratings.csv")
    ratings["section"] = ratings["section"].astype(str)
    if crn:
        return ratings.loc[ratings["crn"] == crn, "rating"].iloc[0] if not ratings.loc[ratings["crn"] == crn].empty else 2.5
    elif course_id and section:
        filtered = ratings[(ratings["course_id"] == course_id) & (ratings["section"] == section)]
        return filtered["rating"].iloc[0] if not filtered.empty else 2.5
    else:
        raise CourseArgumentError

def course_attributes(course_id=None, section=None, crn=None):
    course_data = pd.read_csv("backend/app/Data/class.csv")

    if crn:
        course_data = course_data.loc[course_data["crn"] == crn]
    elif course_id and section:
        course_data["section"] = "1"
        course_data = course_data[(course_data["class_id"] == course_id) & (course_data["section"] == section)]

    else:
        raise CourseArgumentError
    
    course_attributes = { # TODO: Add more attributes based on available data
        "class_name": course_data["class_id"].iloc[0],
        "recurring": course_data["recurring"].iloc[0],
        "prereqs": course_data["prereqs"].iloc[0],
        "requirement_designation": course_data["requirement_designation"].iloc[0],
        "campus": course_data["campus"].iloc[0],
        "class_desc": course_data["class_desc"].iloc[0],
    }
    return course_attributes

def calculate_suitability(preferences, course_id=None, section=None, crn=None):
    if not preferences:
        raise PreferencesError
    if not crn and not course_id and not section:
        raise CourseArgumentError

    attributes = course_attributes(course_id=course_id, section=section, crn=crn)

    RMP_score = rmp_rating(course_id=course_id, section=section, crn=crn)
    GER_score = len(attributes["requirement_designation"].split("with")) if attributes["requirement_designation"] else 0
    
    prereq_groups = attributes["prereqs"].split(";") if attributes["prereqs"] and pd.notna(attributes["prereqs"]) else []
    prereq_score = sum(len(group.split("or")) for group in prereq_groups) / len(prereq_groups) if prereq_groups else 0
    
    campus_score = 1 if attributes["campus"] == preferences.get("campus") else 0
    
    if preferences["class_desc"]:
        from sentence_transformers import SentenceTransformer, util
        model = SentenceTransformer('all-MiniLM-L6-v2')
        class_desc_embeddings = model.encode(attributes["class_desc"], convert_to_tensor=True)
        preferred_desc_embeddings = model.encode(preferences["class_desc"], convert_to_tensor=True)
        similarities = util.pytorch_cos_sim(class_desc_embeddings, preferred_desc_embeddings)
        class_desc_score = float(similarities[0][0])
    else:
        class_desc_score = 0

    # update scores based on preferences
    if preferences.get("rmp") == "high":
        RMP_score *= 2
    else:
        RMP_score = 0
    
    if preferences.get("ger") == "many":
        GER_score *= 2
    else:
        GER_score = 0

    if preferences.get("prereqs") == "few":
        prereq_score = 10 - prereq_score # inverse
        if prereq_score < 0:
            prereq_score = 0 # if more than 10 prereqs then worst score
    else:
        prereq_score = 0
    
    if preferences.get("campus") == attributes["campus"]:
        campus_score *= 2
    else:
        campus_score = 0

    RMP_score /= 5
    GER_score /= 2
    prereq_score /= 10
    campus_score /= 2
    class_desc_score /= 1
    
    scores = [RMP_score, GER_score, prereq_score, campus_score, class_desc_score]
    non_zero_scores = [score for score in scores if score > 0]
    suitability_score = sum(non_zero_scores) / len(non_zero_scores) if non_zero_scores else 0
    return suitability_score

def main():
    # Sample preferences dictionary
    preferences = {
        "rmp": "high",
        "ger": "",
        "prereqs": "few",
        "campus": "",
        "class_desc": "I want to learn about integrals and derivatives."
    }

    suitability_score = calculate_suitability(
        preferences=preferences,
        course_id="Math111",
        section="1"
    )
    print(f"Suitability Score: {suitability_score}")

if __name__ == "__main__":
    main()
