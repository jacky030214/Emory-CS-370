import pandas as pd
import os

df = pd.read_csv("/Users/raasikh/Documents/Coding/spring2025/cs370/schedule_builder/web_scraping/course_data/all_courses.csv")
invalid_crns = df[~df['course_crn'].astype(str).str.isdigit() & df['course_crn'].notna()]
print(invalid_crns)

def clean_crn(crn):
    if isinstance(crn, str) and crn.startswith("['") and crn.endswith("']"):
        return crn.strip("[]'\"")  # removes [, ], ', and "
    return crn

df['course_crn'] = df['course_crn'].apply(clean_crn)
invalid_crns = df[~df['course_crn'].astype(str).str.isdigit() & df['course_crn'].notna()]
print(invalid_crns)

df['credit_hours'] = df['credit_hours'].apply(lambda x: 0 if isinstance(x, str) else x)


df.to_csv("/Users/raasikh/Documents/Coding/spring2025/cs370/schedule_builder/web_scraping/course_data/all_courses.csv", index=False)

exit()
csv1 = "/Users/raasikh/Documents/Coding/spring2025/cs370/schedule_builder/web_scraping/course_data/all_fall_2025_courses.csv"
csv2 = "/Users/raasikh/Documents/Coding/spring2025/cs370/schedule_builder/web_scraping/course_data/all_spring_2025_courses.csv"
output_csv = "/Users/raasikh/Documents/Coding/spring2025/cs370/schedule_builder/web_scraping/course_data/all_courses.csv"

df1 = pd.read_csv(csv1)
df2 = pd.read_csv(csv2)

combined_df = pd.concat([df1, df2], ignore_index=True)
combined_df['temp'] = combined_df['course_code'] + " " + combined_df['course_title']
unique_df = combined_df.drop_duplicates(subset=['temp'])
unique_df = unique_df.drop(columns=['temp'])

unique_df.to_csv(output_csv, index=False)
print(f"Num of unique rows written: {len(unique_df)}")

exit()
csv1 = "/Users/raasikh/Documents/Coding/spring2025/cs370/schedule_builder/web_scraping/course_data/all_fall_2025_oxford_campus_courses.csv"
csv2 = "/Users/raasikh/Documents/Coding/spring2025/cs370/schedule_builder/web_scraping/course_data/all_fall_2025_atlanta_campus_courses.csv"

df1 = pd.read_csv(csv1)
print(f"Number of rows in df1: {len(df1)}")

df2 = pd.read_csv(csv2)
print(f"Number of rows in df2: {len(df2)}")

combined_df = pd.concat([df1, df2], ignore_index=True)
print(f"Number of rows in combined_df: {len(combined_df)}")

combined_df.to_csv("/Users/raasikh/Documents/Coding/spring2025/cs370/schedule_builder/web_scraping/course_data/all_fall_2025_courses.csv", index=False)

print()

csv1 = "/Users/raasikh/Documents/Coding/spring2025/cs370/schedule_builder/web_scraping/course_data/all_spring_2025_oxford_campus_courses.csv"
csv2 = "/Users/raasikh/Documents/Coding/spring2025/cs370/schedule_builder/web_scraping/course_data/all_spring_2025_atlanta_campus_courses.csv"

df1 = pd.read_csv(csv1)
print(f"Number of rows in df1: {len(df1)}")

df2 = pd.read_csv(csv2)
print(f"Number of rows in df2: {len(df2)}")

combined_df = pd.concat([df1, df2], ignore_index=True)
print(f"Number of rows in combined_df: {len(combined_df)}")

combined_df.to_csv("/Users/raasikh/Documents/Coding/spring2025/cs370/schedule_builder/web_scraping/course_data/all_spring_2025_courses.csv", index=False)


exit()
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