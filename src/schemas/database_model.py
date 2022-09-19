from src.constants.constants import *
from src.constants.method_answers import *
from src.schemas.request_model import RequestModel
import json
import os


def get_correct_database_name(database_name: str):
    if not database_name.endswith('.json'):
        database_name += '.json'
    return database_name


class DatabaseModel:
    name: str = None


    def getall_databases(self):
        list_databases = DATABASE.LIST_DATABASES(DATABASE.PATH)
        return {"LIST DATABASES": list_databases}

    def get_database(self, database_name):
        list_databases = DATABASE.LIST_DATABASES(DATABASE.PATH)
        correct_name = get_correct_database_name(database_name)
        if correct_name in list_databases:
            self.name = database_name
            return {"CURRENT DATABASE": self.name}
        return {"NO SUCH DATABASE": database_name}

    def save_test(self, test: RequestModel):
        db_name = get_correct_database_name(self.name)
        with open(DATABASE.PATH + f"/{db_name}") as database:
            try:
                database_json: list = json.loads(database.read())
            except Exception:
                return
        database_json.append(test.dict())
        with open(DATABASE.PATH + f"/{db_name}", mode='w') as database:
            database.write(json.dumps(database_json))
        return {TEST_IS_ADDED.format(test.test_name, self.name)}

    def delete_database(self, database_name):
        list_databases = DATABASE.LIST_DATABASES(DATABASE.PATH)
        filepath = DATABASE.PATH
        for db_name in list_databases:
            if db_name == database_name:
                filepath += f"/{db_name}"
                os.remove(filepath)
                self.name = None
                return {DATABASE_IS_DELETED.format(db_name)}
        return {"STATUS": NO_SUCH.format(DATABASE_STR, database_name)}

    def create_database(self, database_name: str):
        self.name = database_name
        if not database_name.startswith('/'):
            database_name = f"/{database_name}"
        correct_database = get_correct_database_name(database_name)
        with open(PATH.DATABASE + correct_database, mode='w') as database:
            database.write(DATABASE.CREATE)
        return {"STATUS": DATABASE_IS_CREATED.format(self.name)}

    def get_test(self, test_name):
        db_name = get_correct_database_name(self.name)
        with open(DATABASE.PATH + f"/{db_name}") as database:
            data = json.loads(database.read())
        test = [test for test in data if test['test_name'] == test_name]
        if test:
            test: RequestModel = test[0]
            return {"CURRENT TEST": test}, test
        return {NO_SUCH_INTO.format(test_name, self.name)}, None

    def getall_tests(self):
        db_name = get_correct_database_name(self.name)
        with open(DATABASE.PATH + f"/{db_name}") as database:
            data = json.loads(database.read())
        return {"LIST TESTS OF DATABASE {}".format(self.name): data}
