import pandas as pd
import os

csv_dir = '/Users/raasikh/Documents/Coding/spring2025/cs370/schedule_builder/web_scraping/course_data/all'

dfs = []

for filename in sorted(os.listdir(csv_dir)): # make sure order is alphabetical
    if filename.endswith('.csv'):
        file_path = os.path.join(csv_dir, filename)
        df = pd.read_csv(file_path)
        dfs.append(df)

df = pd.concat(dfs, ignore_index=True)

df = df.rename(columns={
    'course_title': 'class_name',
    'course_code': 'class_id',
    "semesters_offered": "recurring",
    'prerequisites': 'prereqs',
    'course_description': 'class_desc',
})

columns_to_keep = [
    'class_name', 'class_id', 'recurring', 'credit_hours', 'prereqs',
    'requirement_designation', 'campus', 'class_desc'
]

df = df[columns_to_keep]
df = df.drop_duplicates()

print(df)
df.to_csv('/Users/raasikh/Documents/Coding/spring2025/cs370/schedule_builder/web_scraping/course_data/all_courses.csv', index=False)