import csv
from .grade_entry import GradeEntry


class CSVReader:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_grades(self):
        grades = []
        start_reading = False

        with open(self.file_path, mode='r', newline='') as file:
            reader = csv.reader(file)
            course_name = next(reader)[0]
            for row in reader:
                if start_reading:
                    grades.append(
                        GradeEntry.from_csv_row(
                            row[:4], course_name
                        )
                    )
                if row[0] == "Class average":
                    start_reading = True

        return grades
