import re
import os
from playwright.sync_api import Page, expect

# def test_has_title(page: Page):
#     page.goto("https://atlas.emory.edu/")

#     # Expect a title "to contain" a substring.
#     expect(page).to_have_title(re.compile("Search Classes"))

def test_has_title(page: Page):

    page.goto("https://atlas.emory.edu/")

    # expects page to have an element with a label containing "Keyword".
    expect(page.get_by_label("Keyword")).to_be_visible()

    page.get_by_label("Keyword").fill("CS")
    page.select_option("select#crit-srcdb", "Spring 2025") # term dropdown

    page.get_by_role("button", name="SEARCH").click()
    page.wait_for_timeout(1000)

    # CSS selector string for all <a> elements with data-group attribute starting with "code:CS "
    course_links = page.query_selector_all("a[data-group^='code:CS ']")

    for idx, link in enumerate(course_links):

        course_data_group = link.get_attribute("data-group") 
        print(course_data_group)

        link.click()
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(1000)
        # page.wait_for_selector("div.panel__body") # add subdiv to wait for here?
        
        # use locator for elements that are updated dynamically instead of a selector which 
        # is static and doesnt work with changing elements (section row changes when clicked)
        section_locator = page.locator("a.course-section.course-section--matched")
        section_texts = section_locator.all_inner_texts()
        print(section_texts)
        print()

        if section_locator.count() == 1: # if there is only one class section, save the page and continue
            with open(f"web_scraping/course_data/course_{idx}_sec_0.html", "w") as f:
                f.write(page.content())
            continue

        for j in range(section_locator.count()):
            row = section_locator.nth(j) # get the nth element dynamically
            print(row.inner_text())
            
            row.click()
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(500)

            with open(f"web_scraping/course_data/course_{idx}_sec_{j}.html", "w") as f:
                f.write(page.content())

            print("-----------------")
            print(page.locator("div.panel.panel--2x.panel--kind-details.panel--visible").text_content())
            print("-----------------")
            exit()
