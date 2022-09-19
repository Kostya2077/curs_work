from copy import deepcopy

import requests
from src.schemas.request_model import RequestModel
import json


class TestRequestModel:

    def run_tests(self, list_request_models=None, result_success=None):
        result_tests = []
        for request_model in list_request_models:
            if isinstance(request_model, dict):
                request_model = RequestModel(**request_model)
            kwargs = {
                "method": request_model.request_method,
                "url": request_model.request_url,
                "headers": request_model.request_headers,
                "cookies": request_model.request_cookie,
                "json": request_model.request_body,
            }
            answer = request_model.answer
            try:
                response = requests.request(**kwargs)
                if answer:
                    result_tests.append(['ok', response, answer, request_model])
                else:
                    result_tests.append(['ok', str(response), None, request_model])
            except Exception as ex:
                result_tests.append([f'ERROR WITH EXCEPTION: [{str(ex)}]', request_model])
        result_tests = self.preprocess_tests(result_tests, result_success)
        return {"TESTS RESULTS:": result_tests}

    def preprocess_tests(self, tests, result_success):
        preprocessed_tests = []
        for test in tests:
            if test[0] == 'ok':
                response, answer, request_model = test[1:]
                current_result = []
                if answer:
                    for key, value in answer.items():
                        if key == 'status':
                            status = response.status_code
                            current_result.append({"status": {"result": value == status,
                                                              "expected": value,
                                                              "response": status}})
                        elif key == 'html':
                            html = response.text
                            current_result.append({'html': {"result": html == answer,
                                                            "expected": value,
                                                            "response": html}})
                        elif key == 'cookie':
                            cookies = value
                            response_cookies = response.cookies
                            tmp = {}
                            for cookie_key in cookies:
                                try:
                                    tmp[cookie_key] = response_cookies.get(cookie_key, '')
                                except Exception:
                                    tmp[cookie_key] = None
                            current_result.append({'cookie': {"result": cookies == tmp,
                                                            "expected": cookies,
                                                            "response": tmp}})
                        elif key == 'headers':
                            headers = value
                            response_headers = response.headers
                            tmp = {}
                            for cookie_key in headers:
                                try:
                                    tmp[cookie_key] = response_headers.get(cookie_key, '')
                                except Exception:
                                    tmp[cookie_key] = None
                            current_result.append({'cookie': {"result": headers == tmp,
                                                            "expected": headers,
                                                            "response": tmp}})
                else:
                    current_result.append({"status": str(response)})
                preprocessed_tests.append({"test": request_model, "test result": deepcopy(current_result)})
            else:
                request_model = test[1]
                preprocessed_tests.append({"test error": request_model, "error value": test[0]})
        return preprocessed_tests
