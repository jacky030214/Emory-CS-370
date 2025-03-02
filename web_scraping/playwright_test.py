import re
import os
from playwright.sync_api import Page, expect
import pandas as pd

def clean_prerequisites(prerequisites: str) -> str:
    """
    A string with prerequisites is cleaned and returned in an appropiate format.
    """
    if not prerequisites:
        return None
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

    # format string according to the required format. Ex: "CS 170 or CS 171; MATH 111"
    prerequisites_str = ""
    for i, or_courses in enumerate(prerequisites):
        prerequisites_str += " or ".join(or_courses)
        if len(prerequisites) - i > 1:
            prerequisites_str += "; "

    return prerequisites_str

def test_scrape_atlas(page: Page):

    page.goto("https://atlas.emory.edu/")

    # expects page to have an element with a label containing "Keyword".
    expect(page.get_by_label("Keyword")).to_be_visible()

    page.get_by_label("Keyword").fill("CS")
    page.select_option("select#crit-srcdb", "Spring 2025") # term dropdown

    page.get_by_role("button", name="SEARCH").click()
    page.wait_for_timeout(1000)

    # CSS selector string for all <a> elements with data-group attribute starting with "code:CS "
    course_links = page.query_selector_all("a[data-group^='code:CS ']")

    for i, link in enumerate(course_links):

        link.click()
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(1000)
        
        # use locator for elements that are updated dynamically instead of a selector which 
        # is static and doesnt work with changing elements (section row changes when clicked)
        section_locator = page.locator("a.course-section.course-section--matched")

        for j in range(section_locator.count()):
            row = section_locator.nth(j) # get the nth element dynamically
            
            row.click(force=True) # skip actionability checks (see https://playwright.dev/python/docs/actionability)
            page.wait_for_timeout(500)

            with open(f"course_data/course_{i}_sec_{j}.html", "w") as f:
                f.write(page.content())

            # print("-----------------")
            # print(page.locator("div.panel.panel--2x.panel--kind-details.panel--visible").text_content()) # all the data that we need
            # print("-----------------")

            # get locators for all course data based on html elements
            course_code = page.locator("div.dtl-course-code")
            course_section_and_crn = page.locator("div.dtl-section")
            course_title = page.locator("div.text.col-8.detail-title.margin--tiny.text--huge")
            credit_hours = page.locator("div.text.detail-hours_html")
            seats = page.locator("div.text.text.detail-seats")
            grading_mode = page.locator("div.text.detail-grademode_code")
            enrollment_status = page.locator("div.text.detail-enrl_stat_html")
            instruction_method = page.locator("div.text.detail-inst_method_code")
            semesters_offered = page.locator("div.text.detail-crse_typoff_html")
            requirement_designation = page.locator("div.text.detail-clss_assoc_rqmnt_designt_html")
            dates = page.locator("div.text.detail-dates_html")
            course_description = page.locator("div.section.section--description div.section__content")
            prerequisites = page.locator("div.section.section--registration_restrictions div.section__content")
            instructor_name = page.locator("div.instructor-name")
            instructor_email = page.locator("div.instructor-email")
            schedule_and_location = page.locator("div.meet")
            final_exam = page.locator("div.section.section--exams_html div.section__content")
            class_type = page.locator("div.course-section-schd")
            campus = page.locator("div.course-section-camp")

            # get text content of each locator if it exists
            course_code = course_code.first.text_content() if course_code.count() > 0 else None
            course_section_and_crn = course_section_and_crn.first.text_content() if course_section_and_crn.count() > 0 else None
            course_title = course_title.first.text_content() if course_title.count() > 0 else None
            credit_hours = credit_hours.first.text_content() if credit_hours.count() > 0 else None
            seats = seats.first.text_content() if seats.count() > 0 else None
            grading_mode = grading_mode.first.text_content() if grading_mode.count() > 0 else None
            enrollment_status = enrollment_status.first.text_content() if enrollment_status.count() > 0 else None
            instruction_method = instruction_method.first.text_content() if instruction_method.count() > 0 else None
            semesters_offered = semesters_offered.first.text_content() if semesters_offered.count() > 0 else None
            requirement_designation = requirement_designation.first.text_content() if requirement_designation.count() > 0 else None
            dates = dates.first.text_content() if dates.count() > 0 else None
            course_description = course_description.first.text_content() if course_description.count() > 0 else None
            prerequisites = prerequisites.first.text_content() if prerequisites.count() > 0 else None
            instructor_name = instructor_name.first.text_content() if instructor_name.count() > 0 else None
            instructor_email = instructor_email.first.text_content() if instructor_email.count() > 0 else None
            schedule_and_location = schedule_and_location.first.text_content() if schedule_and_location.count() > 0 else None
            final_exam = final_exam.first.text_content() if final_exam.count() > 0 else None
            class_type = class_type.first.text_content() if class_type.count() > 0 else None
            campus = campus.first.text_content() if campus.count() > 0 else None

            # for certain data, we need additional cleaning
            course_section, course_crn = re.findall(r"[0-9]+", course_section_and_crn) if course_section_and_crn else (None, None) # find all number values from the string
            credit_hours = credit_hours.strip()[-1] if credit_hours else None
            seats = seats.replace("Seats: ", "") if seats else None
            seats = seats.replace("W", " / W") if seats else None
            grading_mode = grading_mode.replace("Grading Mode: ", "") if grading_mode else None
            enrollment_status = enrollment_status.replace("Enrollment Status: ", "") if enrollment_status else None
            instruction_method = instruction_method.replace("Instruction Method: ", "") if instruction_method else None
            semesters_offered = semesters_offered.replace("Typically Offered: ", "") if semesters_offered else None
            requirement_designation = requirement_designation.replace("Requirement Designation: ", "") if requirement_designation else None
            requirement_designation = re.sub(r"[^\w\s]+", "", requirement_designation) if requirement_designation else None # remove symbols like asteriks
            dates = dates.replace("Dates: ", "") if dates else None
            prerequisites = clean_prerequisites(prerequisites)
            meeting_time, meeting_location = schedule_and_location.split(" in ") if schedule_and_location else (None, None)
            class_type = class_type.replace("Type: ", "").strip() if class_type else None
            campus = campus.replace("Campus: ", "").split("@")[0].strip() if campus else None
            campus = "EM" if campus == "ATL" else campus
            campus = "OX" if campus == "OXF" else campus

            print(course_code)
            print(course_crn)
            print(course_section)
            print(course_title)
            print(credit_hours)
            print(seats)
            print(grading_mode)
            print(enrollment_status)
            print(instruction_method)
            print(semesters_offered)
            print(requirement_designation)
            print(dates)
            print(course_description)
            print(prerequisites)
            print(instructor_name)
            print(instructor_email)
            print(meeting_time)
            print(meeting_location)
            print(final_exam)
            print(class_type)
            print(campus)
            print("\n----------------\n")
            
            if i == 2:
                exit()






