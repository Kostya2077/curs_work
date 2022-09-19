from fastapi import FastAPI
from pydantic import ValidationError

from src.schemas.schemas_ import *

app = FastAPI(
    swagger_ui_parameters={
        'requestSnippetsEnabled': True,
        'Language': 'ru',
    },
)
current_request = RequestModel
current_database = DatabaseModel()
test_request_manager = TestRequestModel()


@app.get("/")
def help():
    return '''Documentation'''


@app.post('/request_model')
def process_request_model(body_params: BodyRequestModel = None):
    global current_request
    method = body_params.method
    if method == 'set':
        current_request = body_params.test_model
        return {"current_test": current_request}
    elif method == 'get':
        try:
            return {"current_test": current_request}
        except Exception:
            return {"current_test": None}
    elif method == 'run':
        try:
            answer = test_request_manager.run_tests(list_request_models=[current_request])
            return answer
        except Exception as ex:
            return f'ERROR WITH EXCEPTION {str(ex)}'
    return {"UNKNOWN COMMAND": method}


@app.post('/database_model')
def process_database_model(body_params: BodyDatabaseModel = None):
    global current_request
    name = body_params.database_name
    method = body_params.method
    test_name = body_params.test_name
    if method == 'get':
        answer = current_database.get_database(name)
        return answer
    elif method == 'getall':
        answer = current_database.getall_databases()
        return answer
    elif method == 'create':
        answer = current_database.create_database(name)
        return answer
    elif method == 'delete':
        answer = current_database.delete_database(name)
        return answer
    elif method == 'save_test' and current_database:
        answer = current_database.save_test(current_request)
        return answer
    elif method == 'get_test':
        answer, test = current_database.get_test(test_name)
        if test:
            current_request = test
        return answer
    elif method == 'getall_tests':
        answer = current_database.getall_tests()
        return answer
    return {"UNKNOWN COMMAND": method}


@app.post('/request_test_model')
def process_request_test_model(body_params: BodyTestRequestModel):
    global current_request
    global current_database
    method = body_params.method
    result_success = body_params.result_success
    db_name = body_params.db_name
    if method == 'run_test':
        try:
            answer = test_request_manager.run_tests(list_request_models=[current_request], result_success=result_success)
            return answer
        except Exception as ex:
            return f'ERROR WITH EXCEPTION: [{str(ex)}]'
    elif method == 'run_tests_of_database':
        if db_name:
            answer = current_database.get_database(db_name)
            for ans_key in answer:
                if 'NO SUCH' in ans_key:
                    return answer
        tests = list(current_database.getall_tests().values())[0]
        try:
            answer = test_request_manager.run_tests(list_request_models=tests, result_success=result_success)
            return answer
        except Exception as ex:
            return f'ERROR WITH EXCEPTION: [{str(ex)}]'
    elif method == 'full_run':
        db_names = list(current_database.getall_databases().values())[0]
        result = []
        for db_name in db_names:
            current_database.get_database(db_name)
            tests = list(current_database.getall_tests().values())[0]
            try:
                answer = test_request_manager.run_tests(list_request_models=tests, result_success=result_success)
                result.append({"database": db_name, 'tests_database': answer})
            except Exception as ex:
                result.append({"database": db_name, 'tests_database': f"ERROR WITH EXCEPTION: [{str(ex)}]"})
        return result
    return {"UNKNOWN COMMAND": method}