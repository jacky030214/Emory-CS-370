import pandas as pd
from itertools import combinations
import datetime

# Load course data
def load_courses(csv_file):
    df = pd.read_csv(csv_file)
    return df

# Parse time strings (e.g., 'MW 1pm-2:15pm') into datetime objects
def parse_meeting_time(time_str):
    if pd.isna(time_str) or time_str.strip() == "":
        return []
    
    days, hours = time_str.split(" ", 1)
    start_time, end_time = hours.split("-")
    
    def convert_to_24hr(time_str):
        try:
            return datetime.datetime.strptime(time_str.strip(), "%I:%M%p").time()
        except ValueError:
            return datetime.datetime.strptime(time_str.strip(), "%I%p").time()
    
    start_dt = convert_to_24hr(start_time)
    end_dt = convert_to_24hr(end_time)
    
    return [(day, start_dt, end_dt) for day in days]

# Check for scheduling conflicts
def has_conflict(schedule, new_course):
    new_times = parse_meeting_time(new_course["meeting_time"])
    for existing_course in schedule:
        existing_times = parse_meeting_time(existing_course["meeting_time"])
        for (new_day, new_start, new_end) in new_times:
            for (exist_day, exist_start, exist_end) in existing_times:
                if new_day == exist_day and (exist_start == new_start or exist_end == new_start or (new_start > exist_start and new_end < exist_start ) or (new_end < exist_end and new_end > exist_start)):
                    return True
    return False

# Generate a schedule based on preferences
def generate_schedule(courses, preferences):
    selected_courses = []
    
    for _, course in courses.iterrows():
        if pd.isna(course["meeting_time"]):
            continue
        
        if (course["enrollment_status"] == "Open" and
            course["seats"].split(" ")[-1] != "0" and
            not has_conflict(selected_courses, course)):
            
            if preferences.get("morning_classes", False):
                meeting_times = parse_meeting_time(course["meeting_time"])
                if all(start.hour >= 12 and end.hour >= 12 for _, start, end in meeting_times):
                    continue
            
            selected_courses.append(course)
        
        if len(selected_courses) >= preferences.get("max_courses", 5):
            break
    
    return selected_courses

# Example usage
if __name__ == "__main__":
    courses_df = load_courses("/Users/raasikh/Documents/Coding/spring2025/cs370/schedule_builder/web_scraping/course_data/all_courses.csv")
    preferences = {
        "morning_classes": True,
        "max_courses": 4
    }
    schedule = generate_schedule(courses_df, preferences)
    
    for course in schedule:
        print(course[["course_code", "meeting_time", "instructor_name"]].to_string(index=False))
        print()