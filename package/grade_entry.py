class GradeEntry:
    def __init__(self, firstname, lastname, email, overall_grade, course) -> None:
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.overall_grade = overall_grade
        self.course = course

    @classmethod
    def from_csv_row(cls, row: list, course: str):
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
