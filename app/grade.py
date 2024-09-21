import csv
import openpyxl

from typing import Iterable


class GradeEntry:
    def __init__(self, firstname, lastname, email, overall_grade, course) -> None:
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.overall_grade = overall_grade
        self.course = course

    @classmethod
    def from_csv_row(cls, row: list, course: str | None = None):
        overall_grade = f"{row[3] * 100: .2f}%"
        return cls(
            row[1],
            row[0],
            row[2],
            overall_grade,
            course,
        )

    def to_dict(self):
        return {
            "First_Name__c": self.firstname,
            "Last_Name__c": self.lastname,
            "Email__c": self.email,
            "Overall_Grade__c": self.overall_grade,
            "Course__c": self.course,
        }

    def __str__(self) -> str:
        return f"{self.email} : {self.overall_grade}"

    def __repr__(self) -> str:
        return f"GradeEntry({self.firstname}, {self.lastname}, {self.email}, {self.overall_grade}, {self.course})"


class GradeReader:

    def __read_grades(self, data: Iterable):
        grades = []
        start_reading = False
        for row in data:

            # prevent index out of range for the last row of the sheet
            if start_reading and not row:
                break

            if start_reading:
                grade = GradeEntry.from_csv_row(row)
                print(grade)
                grades.append(grade)

            if row[0] == "Class average":
                start_reading = True

        return grades

    def read_grades_from_list(self, data: list[list[str]]) -> list[GradeEntry]:
        course_name = data[0][0]
        grades = self.__read_grades(data)
        for grade in grades:
            grade.course = course_name
        return grades

    def read_grades_from_csv(self, file_path):
        with open(file_path, mode='r', newline='') as file:
            reader = csv.reader(file)
            course_name = next(reader)[0]
            grades = self.__read_grades(reader)
            for grade in grades:
                grade.course = course_name

        return grades

    def read_grades_from_xlsx(self, file_path):
        wb = openpyxl.load_workbook(file_path, True, data_only=True)
        sheet = wb.active
        data = sheet.values
        course_name = next(data)[0]
        grades = self.__read_grades(data)
        for grade in grades:
            grade.course = course_name
        return grades
