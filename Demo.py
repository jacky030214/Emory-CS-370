from Class_Detail_Model import Class_Detail
from Professor_Model import Professor
from Semster_Schedule_Model import Semester_Schedule

def main():
    # Create a Professor object
    Turing = Professor(
        name="Dr. Turing",
        email="alan.turing@university.edu",
        ratemyprof_score=4.9,
        ratemyprof_tags=["Brilliant", "Challenging"]
    )

    # Create a Class_Detail (subclass of ClassModel) with nested Professor
    CS201 = Class_Detail(
        class_id="CS201",
        class_number="201",
        class_name="Advanced Computer Science",
        recurring="every Spring",
        credit_hours=4,
        prereqs=["CS101"],
        requirement_designation=["Core"],
        campus="EM",
        class_desc="Deep dive into advanced topics.",
        section="B",
        professor=Turing,  # pass the Professor object
        time_slot="10:00-10:50",
        days=["Mon", "Wed", "Fri"],
        class_size=25,
        offering="inperson",
        room="Room 202"
    )
    
    # Create a schedule for 2025 Spring
    spring_2025_schedule = Semester_Schedule(year=2025, semester="Spring")
    
    # Put class into schedule
    for day in CS201.days:
        # Normalize or map day abbreviations to schedule attributes
        # You can expand or customize this mapping as needed
        day_map = {
            "Mon": "monday",
            "Tue": "tuesday",
            "Wed": "wednesday",
            "Thur": "thursday",
            "Fri": "friday",
        }

        # Check if our mapping recognizes this day
        schedule_attr = day_map.get(day)
        if schedule_attr is not None:
            getattr(spring_2025_schedule, schedule_attr).append(CS201)
        else:
            # If it's an unexpected day string, handle or log an error here
            print(f"Warning: Unrecognized day '{day}' for class {CS201.class_id}")

    # 5. Print out the schedule
    print("Semester Schedule object:\n", spring_2025_schedule)

    # 6. Convert the schedule to a dict (for database insertion)
    schedule_dict = spring_2025_schedule.to_dict()
    print("\nSerialized schedule (dict) to store in DB:\n", schedule_dict)

    # 7. Reconstruct the schedule from that dict
    restored_schedule = Semester_Schedule.from_dict(schedule_dict)
    print("\nRestored schedule from dict:\n", restored_schedule)


if __name__ == "__main__":
    main()