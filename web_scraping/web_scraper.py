# RUN THIS WITH the pytest cmd, optionally with --headed flag to see the browser in action
# or you can run the program as main

import re
import os
from playwright.sync_api import Page, expect, ElementHandle
from typing import List
import pandas as pd
import logging


logging.basicConfig(
    filename="scraper_debug.log",  # Log file
    level=logging.DEBUG,  # Log all debug info
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="w",
)

# helper function
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

    # format string according to the required format. Ex: "CS170 or CS171; MATH111"
    for i, or_courses in enumerate(prerequisites):
        for j, course in enumerate(or_courses):
            prerequisites[i][j] = course.replace(" ", "")
    
    prerequisites_str = ""
    for i, or_courses in enumerate(prerequisites):
        prerequisites_str += " or ".join(or_courses)
        if len(prerequisites) - i > 1: # if we are not at the last set of or_courses
            prerequisites_str += "; "

    return prerequisites_str

# helper function
def clean_semesters_offered(semesters_offered: str) -> str:
    """
    A string with semesters offered is cleaned and returned in an appropiate format.
    """
    if not semesters_offered:
        return None
    if semesters_offered.__contains__("Fall") and semesters_offered.__contains__("Spring") and semesters_offered.__contains__("Summer"):
        return "fall/spring/summer"
    if semesters_offered.__contains__("Fall") and semesters_offered.__contains__("Spring"):
        return "fall/spring"
    if semesters_offered.__contains__("Fall"):
        return "fall"
    if semesters_offered.__contains__("Spring"):
        return "spring"
    if semesters_offered.__contains__("Summer"):
        return "summer"
    return None

# helper function
def get_start_index(course_links: List[ElementHandle]) -> int:
    """
    Determines the starting index for scraping by checking if there is a record of the last scraped course.
    """
    last_course_code_path = "/Users/raasikh/Documents/Coding/spring2025/cs370/schedule_builder/web_scraping/last_course_code.txt"
    if os.path.exists(last_course_code_path):
        with open(last_course_code_path, "r") as f:
            last_course_code = f.read().strip()
            if last_course_code == "COMPLETE":
                return 0
            last_course_code = re.sub(r'([a-zA-Z])(\d)', r'\1 \2', last_course_code) # add space bw course code prefix and num
        for i, link in enumerate(course_links):
            if last_course_code in link.inner_text():
                return i+1
    return 0

# main scraping function
def test_scrape_atlas(page: Page):
    
    """
    Adjustable Parameters
    """
    # create a dictionary to store all the desired course data
    course_data = {
        "course_code": [],
        "course_section": [],
        "course_crn": [],
        "course_title": [],
        "credit_hours": [],
        "seats": [],
        "grading_mode": [],
        "enrollment_status": [],
        "instruction_method": [],
        "semesters_offered": [],
        "requirement_designation": [],
        "dates": [],
        "course_description": [],
        "prerequisites": [],
        "instructor_name": [],
        "instructor_email": [],
        "meeting_time": [],
        "meeting_location": [],
        "final_exam": [],
        "class_type": [],
        "campus": []
    } # if adjusted, make sure to adjust the csv output below
    searchword = "" # empty for all courses in selected semester and at selected campus
    search_semester = "Fall 2025"
    search_campus = "Oxford Campus"

    """
    Web-scraping Begins
    """

    page.goto("https://atlas.emory.edu/")

    # # expects page to have an element with a label containing "Keyword".
    # expect(page.get_by_label("Keyword")).to_be_visible()

    page.get_by_label("Keyword").fill(searchword)
    page.select_option("select#crit-srcdb", search_semester)
    page.select_option("select#crit-camp", search_campus)

    page.get_by_role("button", name="SEARCH").click()
    page.wait_for_selector("div.panel__info-bar")
    page.wait_for_timeout(1000)

    # CSS selector string for all <a> elements with data-group attribute starting with "code:"
    course_links = page.query_selector_all("div.result.result--group-start a.result__link")

    # see where to start off the loop from if the scraper failed in between before
    start_index = get_start_index(course_links)

    logging.info(f"Found {len(course_links)} course links")
    print(f"Found {len(course_links)} course links")

    try:
        for i, link in enumerate(course_links[start_index:], start=start_index):

            logging.info(f"Trying to click link {i+1}: {link.inner_text()}")
            print(f"Working on {link.inner_text().split("\n")[0]}")
            try:
            # the following checks are needed since the webpage updates dynamically
                link.scroll_into_view_if_needed()
                link.wait_for_element_state("stable")
                link.click(force=True)
                
                logging.info(f"Successfully clicked link {i+1}: {link.inner_text()}")
            
                page.wait_for_load_state("networkidle")
                page.wait_for_selector("div.dtl-course-code")
                page.wait_for_timeout(1000)
            except Exception as e:
                logging.error(f"An exception occurred while clicking on the course. Trying to continue: {e}")
            
            # use locator for elements that are updated dynamically instead of a selector which 
            # is static and doesnt work with changing elements (section row changes when clicked)
            section_locator = page.locator("a.course-section.course-section--matched")

            for j in range(section_locator.count()):
                
                try:
                    row = section_locator.nth(j) # get the nth element dynamically

                    row.click(force=True) # skip actionability checks (see https://playwright.dev/python/docs/actionability)
                    page.wait_for_load_state("networkidle")
                    page.wait_for_selector("div.course-sections")
                    page.wait_for_timeout(500)
                except Exception as e:
                    logging.error(f"An exception occurred while clicking on course section. Trying to continue: {e}")

                # with open(f"web_scraping/course_data/course_{i}_sec_{j}.html", "w") as f:
                #     f.write(page.content())

                # print("-----------------")
                # print(page.locator("div.panel.panel--2x.panel--kind-details.panel--visible").text_content()) # all the data that we need
                # print("-----------------")

                # get locators for all course data based on html elements
                course_code = page.locator("div.dtl-course-code")
                course_section_and_crn = page.locator("div.dtl-section")
                while not course_section_and_crn:
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
                if course_section_and_crn:
                    course_section_and_crn = re.findall(r"[0-9]+", course_section_and_crn)
                    if len(course_section_and_crn) == 1:
                        course_crn = course_section_and_crn
                        course_section = None
                    else:
                        course_section, course_crn = course_section_and_crn[0], course_section_and_crn[1]
                else:
                    course_section, course_crn = (None, None)
                credit_hours = credit_hours.strip()[-1] if credit_hours else None
                seats = seats.replace("Seats: ", "") if seats else None
                seats = seats.replace("W", " / W") if seats else None
                grading_mode = grading_mode.replace("Grading Mode: ", "") if grading_mode else None
                enrollment_status = enrollment_status.replace("Enrollment Status: ", "") if enrollment_status else None
                instruction_method = instruction_method.replace("Instruction Method: ", "") if instruction_method else None
                semesters_offered = semesters_offered.replace("Typically Offered: ", "") if semesters_offered else None
                semesters_offered = clean_semesters_offered(semesters_offered) if semesters_offered else None
                requirement_designation = requirement_designation.replace("Requirement Designation: ", "") if requirement_designation else None
                requirement_designation = re.sub(r"[^\w\s]+", "", requirement_designation) if requirement_designation else None # remove symbols like asteriks
                dates = dates.replace("Dates: ", "") if dates else None
                prerequisites = clean_prerequisites(prerequisites)
                if schedule_and_location and "in" not in schedule_and_location.lower():
                    if "am" in schedule_and_location.lower() or "pm" in schedule_and_location.lower():
                        meeting_time = schedule_and_location
                    else:
                        meeting_location = schedule_and_location
                else:
                    meeting_time, meeting_location = schedule_and_location.split(" in ") if schedule_and_location else (None, None)
                class_type = class_type.replace("Type: ", "").strip() if class_type else None
                campus = campus.replace("Campus: ", "").split("@")[0].strip() if campus else None
                campus = "EM" if campus == "ATL" else campus
                campus = "OX" if campus == "OXF" else campus
                course_description = course_description.replace("\n", " ") if course_description else None
                course_code = course_code.replace(" ", "") if course_code else None

                # append to course data dictionary
                # adjust this based on desired csv output
                course_data["course_code"].append(course_code)
                course_data["course_section"].append(course_section)
                course_data["course_crn"].append(course_crn)
                course_data["course_title"].append(course_title)
                course_data["credit_hours"].append(credit_hours)
                course_data["seats"].append(seats)
                course_data["grading_mode"].append(grading_mode)
                course_data["enrollment_status"].append(enrollment_status)
                course_data["instruction_method"].append(instruction_method)
                course_data["semesters_offered"].append(semesters_offered)
                course_data["requirement_designation"].append(requirement_designation)
                course_data["dates"].append(dates)
                course_data["course_description"].append(course_description)
                course_data["prerequisites"].append(prerequisites)
                course_data["instructor_name"].append(instructor_name)
                course_data["instructor_email"].append(instructor_email)
                course_data["meeting_time"].append(meeting_time)
                course_data["meeting_location"].append(meeting_location)
                course_data["final_exam"].append(final_exam)
                course_data["class_type"].append(class_type)
                course_data["campus"].append(campus)

        # save a csv
        df = pd.DataFrame(course_data)
        searchword = "all" if searchword == "" else searchword.replace(" ", "_").lower()
        search_semester = search_semester.replace(" ", "_").lower()
        search_campus = search_campus.replace(" ", "_").lower()
        df.to_csv(f"/Users/raasikh/Documents/Coding/spring2025/cs370/schedule_builder/web_scraping/course_data/{searchword}_{search_semester}_{search_campus}_courses.csv", index=False)
        with open("/Users/raasikh/Documents/Coding/spring2025/cs370/schedule_builder/web_scraping/last_course_code.txt", "w") as f:
            f.write("COMPLETE")

    except Exception as e:
        try:
            t = link.inner_text()
        except:
            t = None
        try:
            r = row.text_content()
        except:
            r = None

        logging.error(f"ERROR: {e};\nLINK: {t};\nROW: {r}")
        with open("/Users/raasikh/Documents/Coding/spring2025/cs370/schedule_builder/web_scraping/last_course_code.txt", "w") as f:
            f.write(course_code if course_code else "")
        df = pd.DataFrame(course_data)
        searchword = "all" if searchword == "" else searchword.replace(" ", "_").lower()
        search_semester = search_semester.replace(" ", "_").lower()
        search_campus = search_campus.replace(" ", "_").lower()
        df.to_csv(f"/Users/raasikh/Documents/Coding/spring2025/cs370/schedule_builder/web_scraping/course_data/INCOMPLETE_{searchword}_{search_semester}_{search_campus}_courses.csv", index=False)
        raise

# if run without pytest
if __name__ == "__main__":
    from playwright.sync_api import sync_playwright
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        test_scrape_atlas(page)

        browser.close()