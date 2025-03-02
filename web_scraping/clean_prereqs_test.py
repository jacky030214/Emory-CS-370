import re

pqs = ["This course requires CS 170 OR CS_OX 170 or equivalent transfer credit as a prerequisite.",
       "(MATH 111 or MATH_OX 111 or QTM 100 or QTM_OX 100) and (CS 110 or CS 170 or CS_OX 170) or equivalent transfer credit as prerequisites.",
       "(CS 170 or CS_OX 170) and (MATH 111 or MATH_OX 111) or equivalent transfer credit as prerequisites.",
       "CS 171 or 171Z or CS_OX 171 or equivalent transfer credit as a prerequisite.", # 171Z WILL NOT BE CAUGHT BY REGEX
       "This course requires CS 171 or CS 171Z or CS_OX 171 or equivalent transfer credit as a prerequisite.",
       "(CS 224 or CS_OX 224) and CS 253 or equivalent transfer credit as prerequisite.",
       "(CS 170 or CS_OX 170) and (CS 171 or CS_OX 171) and (CS 224 or CS_OX 224) and CS 253, or equivalent transfer credit as prerequisite.",
       "This course requires CS 171 or CS 171Z or CS_OX 171 or equivalent transfer credit as a prerequisite.",
       "(CS224 or CS_OX 224) and (CS 253 or CS_OX 253) and (MATH 221 or MATH_OX 221 or MATH 275 or MATH 321) or equivalent transfer credit as prerequisite.",
       "CS 253 and CS 255 or equivalent transfer credit as prerequisites.",
       "CS 253 or equivalent transfer credit as prerequisite.",
       "CS 253 or CS_OX 253 or equivalent transfer credit as prerequisite.",

"""Prerequisite: CS 253
Department permission required, please email bnflood@emory.edu""",

"""
Prerequisite: CS 253
Department permission required, please email bnflood@emory.edu
This class focuses on identifying and building interactive systems. This will include how to specify, design, and build user interfaces and systems that enable interactivity. Work will be justified in terms of how technical design choices enable or inhibit the user experience. The course will cover a variety of tools and techniques for creating interactive prototypes and user interfaces, examine their advantages and trade-offs for investigating and enabling user experience, and the related theory and principles for their implementation.""",

"ECON 320 & CS 334 or equivalent transfer credit as prerequisites."]

for j, prerequisites in enumerate(pqs):
    prerequisites = prerequisites.split(" and ")
    
    compounds_to_remove = [] # store compound prereqs with "&" to remove (ex: CS 170 & CS 171)
    for i, prereq in enumerate(prerequisites):
        if len(prereq.split("&")) > 1:
            prerequisites += prereq.split("&")
            compounds_to_remove.append(prereq)
    
    for compound in compounds_to_remove:
        prerequisites.remove(compound)
    
    for i, prereq in enumerate(prerequisites):
        prerequisites[i] = re.findall(r"[A-Z]+_?[A-Z]+?\s?[0-9]+[A-Z]?+", prereq) # pattern to find all course codes

    prerequisites = [prereq for prereq in prerequisites if prereq] # remove empty arrays

    prerequisites_str = ""
    
    # remove spaces within course codes
    for i, or_courses in enumerate(prerequisites):
        for j, course in enumerate(or_courses):
            prerequisites[i][j] = course.replace(" ", "")

    for i, or_courses in enumerate(prerequisites):
        prerequisites_str += " or ".join(or_courses)
        if len(prerequisites) - i > 1:
            prerequisites_str += "; "

    print(j, prerequisites_str)
    # prerequisites = "".join(prerequisites)
    # prerequisites = re.sub(r"[\(\)]", "", prerequisites) # remove brackets
    # prerequisites = prerequisites.replace(" and ", "; ")
    # print(prerequisites + "\n")
    print("----")