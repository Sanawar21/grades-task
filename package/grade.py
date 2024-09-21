import csv
import typing
import openpyxl


class GradeEntry:
    def __init__(self, firstname, lastname, email, overall_grade, course) -> None:
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.overall_grade = overall_grade
        self.course = course

    @classmethod
    def from_csv_row(cls, row: list, course: str | None = None):
        return cls(
            row[1],
            row[0],
            row[2],
            row[3],
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
        return f"{self.email} - {self.course}: {self.overall_grade}"


class GradeReader:

    def __read_grades(self, data: typing.Iterable):
        grades = []
        start_reading = False
        for row in data:
            if start_reading:
                grades.append(
                    GradeEntry.from_csv_row(row)
                )
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
        wb = openpyxl.load_workbook(file_path)
        sheet = wb.active
        data = sheet.values
        course_name = next(data)[0]
        grades = self.__read_grades(data)
        for grade in grades:
            grade.course = course_name
        return grades
