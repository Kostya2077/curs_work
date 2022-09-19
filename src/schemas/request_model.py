from typing import *
from pydantic import BaseModel


class RequestModel(BaseModel):
    test_name: str
    request_method: str
    request_url: str
    request_headers: Dict = None
    request_cookie: Dict = None
    request_body: Dict = None
    answer: Dict = None

    def get_dict(self):
        return {
            "test_name": self.test_name,
            "request_method": self.request_method,
            "request_url": self.request_url,
            "request_headers": self.request_headers,
            "request_cookie": self.request_cookie,
            "request_body": self.request_body,
            "answer": self.answer,
        }



