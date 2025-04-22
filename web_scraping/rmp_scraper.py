from playwright.sync_api import sync_playwright
from tqdm import tqdm
import pandas as pd

oxford_url = "https://www.ratemyprofessors.com/search/professors/2633?q="
emory_url = f"https://www.ratemyprofessors.com/search/professors/340?q="
data = []

for url in [emory_url, oxford_url]:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url, wait_until="domcontentloaded")
        print("gone to page; waiting for button")
        page.wait_for_selector('button:has-text("Show More")', timeout=5000)
        print("waiting for button done")
        counter = 1

        while True:
            try:
                show_more_button = page.query_selector('button:has-text("Show More")')
                show_more_button.click()
                print(f"\rclicked show more button x{counter}", end="")
                counter += 1
                # wait until the button is not disabled 
                page.wait_for_function(
                    "(btn) => !btn.disabled",
                    arg=show_more_button,
                    timeout=10000
                )
            except:
                print("\nno more show more button")
                break
        
        result_a_tags = page.query_selector_all("div.SearchResultsPage__StyledResultsWrapper-vhbycj-4 a")
        for a in tqdm(result_a_tags, desc="Getting professor ratings..."):
            rating_div = a.query_selector("div.CardNumRating__CardNumRatingNumber-sc-17t4b9u-2")
            rating = rating_div.inner_text().strip() if rating_div else "N/A"

            name_div = a.query_selector("div.CardName__StyledCardName-sc-1gyrgim-0")
            name = name_div.inner_text().strip() if name_div else "N/A"

            data.append({"name": name, "rating": rating})

    print(f"done with {url}\n")

df = pd.DataFrame(data)
df.to_csv("/Users/raasikh/Documents/Coding/spring2025/cs370/schedule_builder/web_scraping/course_data/professor_ratings.csv", index=False)