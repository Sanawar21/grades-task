from simple_salesforce import SalesforceLogin, SFType
from abc import ABC, abstractmethod
from .grade import GradeEntry
from typing import Literal


class AbstractSalesforceClient(ABC, SFType):
    def __init__(self, username, password, security_token, object_name, domain: Literal["login", "test"]):
        session_id, instance = SalesforceLogin(
            username=username,
            domain=domain,
            password=password,
            security_token=security_token
        )
        SFType.__init__(self, object_name, session_id, instance)

    @abstractmethod
    def upload(self, data: dict):
        """Uploads an object to Salesforce"""
        pass


class GradesClient(AbstractSalesforceClient):
    def __init__(self, username, password, security_token, domain):
        super().__init__(
            username,
            password,
            security_token,
            "hed__Term_Grade__c",
            domain,
        )

    def upload(self, grade_entry: GradeEntry):
        data = grade_entry.to_dict()
        # TODO: Remove this
        data["hed__Course_Connection__c"] = "a03Au00000jc73eIAA"
        return self.create(data)
