def convert_to_24_hour(time_str):
        time_str = time_str.lower().replace(":", "") # 9:00am -> 900am or 2:00pm -> 200pm
        if "am" in time_str:
            time_str = time_str.replace("am", "")
            time_num = int(time_str)
            if time_num == 1200:  # handle 12:00am as 0
                return 0
            return time_num
        else:
            time_str = time_str.replace("pm", "")
            time_num = int(time_str)
            if time_num == 1200:  # add 12 hours for pm times except 12pm
                return time_num
            return time_num + 1200

def parse_course_time(course_time: str) -> tuple[list[str], str, str]:
    course_time = course_time.split(" ")
    course_days_str = course_time[0]
    course_days = []
    if course_days_str.__contains__("M"):
        course_days.append("M")
        course_days_str = course_days_str.replace("M", "")
    if course_days_str.__contains__("W"):
        course_days.append("W")
        course_days_str = course_days_str.replace("W", "")
    if course_days_str.__contains__("Th"):
        course_days.append("Th")
        course_days_str = course_days_str.replace("Th", "")
    if course_days_str.__contains__("T"):
        course_days.append("T")
        course_days_str = course_days_str.replace("T", "")
    if course_days_str.__contains__("F"):
        course_days.append("F")
        course_days_str = course_days_str.replace("F", "")
    
    course_hours = course_time[1].split("-")
    course_start = course_hours[0]
    if not course_start.__contains__(":"):
        if course_start.__contains__("am"):
            course_start = course_start.replace("am", ":00am")
        else:
            course_start = course_start.replace("pm", ":00pm")
    course_end = course_hours[1]
    if not course_end.__contains__(":"):
        if course_end.__contains__("am"):
            course_end = course_end.replace("am", ":00am")
        else:
            course_end = course_end.replace("pm", ":00pm")

    course_start = convert_to_24_hour(course_start)
    course_end = convert_to_24_hour(course_end)
    return course_days, course_start, course_end

import unittest

class TestFunctions(unittest.TestCase):

    def test_convert_to_24_hour(self):
        # Test AM times
        self.assertEqual(convert_to_24_hour("9:00am"), 900)
        self.assertEqual(convert_to_24_hour("12:00am"), 0)
        self.assertEqual(convert_to_24_hour("11:59am"), 1159)

        # Test PM times
        self.assertEqual(convert_to_24_hour("2:00pm"), 1400)
        self.assertEqual(convert_to_24_hour("12:00pm"), 1200)
        self.assertEqual(convert_to_24_hour("11:59pm"), 2359)

    def test_parse_course_time(self):
        # Test single day
        self.assertEqual(parse_course_time("M 9:00am-10:00am"), (["M"], 900, 1000))
        self.assertEqual(parse_course_time("F 1:00pm-2:30pm"), (["F"], 1300, 1430))

        # Test multiple days
        self.assertEqual(parse_course_time("MWF 9:00am-10:00am"), (["M", "W", "F"], 900, 1000))
        self.assertEqual(parse_course_time("TTh 2:00pm-3:15pm"), (["Th", "T"], 1400, 1515))

        # Test edge cases
        self.assertEqual(parse_course_time("MWThF 12:00am-12:00pm"), (["M", "W", "Th", "F"], 0, 1200))
        self.assertEqual(parse_course_time("T 11:59pm-12:00am"), (["T"], 2359, 0))

if __name__ == "__main__":
    unittest.main()