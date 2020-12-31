import json
import os
from lib import ErrorHandler
import re


class Structure:

    def __init__(self):
        self._structure = None

    def Create(self, database_name: str):

        try:
            if os.path.exists("./databases/"):
                pass
            else:
                os.mkdir(f"./databases/")

        except:
            raise Exception(f'Error creating Databases folder at {os.path.abspath("./databases/")}')

        try:
            if os.path.exists(f"./databases/{database_name}"):
                print(f'Database "{database_name}" already exists')
                pass

            else:
                os.mkdir(f"./databases/{database_name}")
                os.mkdir(f"./databases/{database_name}/schemas")
                return self._structure

        except:
            raise ErrorHandler.DatabaseCreation(database_name)

    def AddTable(self, database_name: str, table_name: str):

        if isinstance(table_name, str):
            if os.path.exists(f'./databases/{database_name}/schemas/{table_name}.schema.fdb'):
                print(f'Table "{table_name}" already exists')
                pass
            else:
                my_dict = {table_name: {'schema': {}}}

                with open(f'./databases/{database_name}/schemas/{table_name}.schema.fdb', 'w') as FILE:
                    FILE.write(json.dumps(my_dict, indent=4))

            if os.path.exists(f'./databases/{database_name}/{table_name}.fdb'):
                pass
            else:
                open(f'./databases/{database_name}/{table_name}.fdb', "w")
            return self._structure

        else:
            for i in table_name:
                if os.path.exists(f'./databases/{database_name}/schemas/{i}.schema.fdb'):
                    print(f'Table "{i}" already exists')
                    pass
                else:
                    my_dict = {i: {'schema': {}}}
                    print(my_dict)
                    with open(f'./databases/{database_name}/schemas/{i}.schema.fdb', 'w') as FILE:
                        FILE.write(json.dumps(my_dict, indent=4))

                if os.path.exists(f'./databases/{database_name}/{i}.fdb'):
                    pass

                else:
                    open(f'./databases/{database_name}/{i}.fdb', "w")
            return self._structure

    def AddField(self, database_name: str, table_name: str, field_name):

        data = Structure._LoadData(self, database_name, table_name)
        if isinstance(field_name, str):
            if field_name in data[table_name]['schema'].keys():
                print(f'Field name "{field_name}" already exists')
                pass
            else:
                data[table_name]['schema'][field_name] = {'Required': False, 'Type': 'str', 'MinLen': 3, 'MaxLen': 10}
                print(
                    f'Field Variables auto generated, to edit go into {os.path.abspath(f"{table_name}.schema.fdb to change")}')
                Structure._SaveData(self, database_name, table_name, data)
        else:
            for i in field_name:
                if i in data[table_name]['schema'].keys():
                    print(f'Field name "{i}" already exists')
                    pass
                else:
                    data[table_name]['schema'][i] = {'Required': False, 'Type': 'str', 'MinLen': 3, 'MaxLen': 10,
                                                     'Duplicates': False}
                    print(
                        f'Field Variables auto generated, to edit go into {os.path.abspath(f"{table_name}.schema.fdb to change")}')
                    Structure._SaveData(self, database_name, table_name, data)

    def _LoadData(self, database_name, table_name):

        try:
            with open(f'./databases/{database_name}/schemas/{table_name}.schema.fdb', 'r') as FILE:
                self._structure = json.load(FILE)

            return self._structure

        except:
            raise ErrorHandler.LoadData(database_name, table_name)

    def _SaveData(self, database_name, table_name, data):

        try:
            with open(f'./databases/{database_name}/schemas/{table_name}.schema.fdb', 'w') as FILE:
                FILE.write(json.dumps(data, indent=4))

            return self._structure

        except:
            raise ErrorHandler.SaveData(database_name)


class database:

    def __init__(self):
        self._structure = None
        self._database_name = None
        self._table_name = None

    def SelectDB(self, database_name: str):
        self._database_name = database_name

    def SelectTable(self, table_name: str):
        self._table_name = table_name
        try:
            with open(f'./databases/{self._database_name}/schemas/{self._table_name}.schema.fdb', 'r') as FILE:
                data = json.load(FILE)
            self._structure = data[table_name]['schema']
        except:
            raise ErrorHandler.SelectTable(self._database_name, self._table_name)

    def Insert(self, contents):
        database_name = self._database_name
        table_name = self._table_name

        def _SaveData(db, tbl, content):

            content = re.sub("\s+", "", json.dumps(content))

            with open(f'./databases/{db}/{tbl}.fdb', 'a') as FILE:
                FILE.write(content + '\n')

        for field, desc in self._structure.items():
            if 'Required' in desc:

                if desc['Required'] and field not in contents:
                    raise ErrorHandler.InvalidField(field)

        for field, value in contents.items():

            if field not in self._structure:
                raise ErrorHandler.InvalidField(field)

            if self._structure[field]['Required'] and not value or value.isspace():
                raise ErrorHandler.EmptyValue(field, 'Required', self._structure[field]['Required'])
            if type(value).__name__ != self._structure[field]['Type']:
                raise ErrorHandler.Type(value, self._structure[field]['Type'])

            if "MinLen" in self._structure[field]:
                if len(value) < self._structure[field]['MinLen']:
                    raise ErrorHandler.MinLength(value, self._structure[field]['MinLen'])

            if "MaxLen" in self._structure[field]:
                if len(value) > self._structure[field]['MaxLen']:
                    raise ErrorHandler.MaxLength(value, self._structure[field]['MaxLen'])

            temp_content = re.sub("\s+", "", str(contents))

            if not self._structure[field]['Duplicates']:
                if os.path.exists(f'./databases/{self._database_name}/{self._table_name}.fdb'):
                    if re.search(f'({temp_content})', open(f'./databases/{self._database_name}/{self._table_name}.fdb',
                                                           'r').read()) is not None:
                        raise ErrorHandler.Duplicate(temp_content)
                else:
                    pass

        _SaveData(database_name, table_name, contents)

    def Get(self, entry: dict):

        output = None

        with open(f'./databases/{self._database_name}/{self._table_name}.fdb') as file:
            data = file.read()

            entries = [f"\"{k}\":\"{v}\"" for k, v in entry.items()]
            filtered = [e[0] for e in (re.findall(f"({{(.+)?({entries[0]})(.+)?}}+)", data))]

            if len(filtered) != 0:
                for i in filtered:
                    matched = 0

                    for e in entries:
                        if re.search(f"{e}", i) is not None:
                            matched += 1

                    if matched == len(entry.keys()):
                        output = json.loads(i)
                        break
                return output
            else:
                print(f'"{entries}" is/are not in the table "{self._table_name}"')
                return None

    def GetAll(self, entry: dict):

        output = []

        with open(f'./databases/{self._database_name}/{self._table_name}.fdb') as file:
            data = file.read()

            entries = [f"\"{k}\":\"{v}\"" for k, v in entry.items()]
            filtered = [e[0] for e in (re.findall(f"({{(.+)?({entries[0]})(.+)?}}+)", data))]

            if len(filtered) != 0:
                for i in filtered:
                    matched = 0

                    for e in entries:
                        if re.search(f"{e}", i) is not None:
                            matched += 1

                    if matched == len(entry.keys()):
                        output.append(json.loads(i))
                return output
            else:
                print(f'"{entries}" is/are not in the table "{self._table_name}"')
                return None

    def Delete(self, entry: dict):

        with open(f'./databases/{self._database_name}/{self._table_name}.fdb') as file:
            data = file.read()

            entries = [f"\"{k}\":\"{v}\"" for k, v in entry.items()]
            filtered = [e[0] for e in (re.findall(f"({{(.+)?({entries[0]})(.+)?}}+)", data))]

            if len(filtered) != 0:
                for i in filtered:
                    matched = 0

                    for e in entries:
                        if re.search(f"{e}", i) is not None:
                            matched += 1

                    if matched == len(entry.keys()):

                        with open(f'./databases/{self._database_name}/{self._table_name}.fdb', "w") as FILE:
                            data = re.sub(r'\n\s*\n', '\n', data.replace(i, "", 1), re.MULTILINE)
                            FILE.write(data)

                        with open(f'./databases/{self._database_name}/{self._table_name}.fdb', "r+") as fi:
                            data = json.loads(fi.read())

                            fi.seek(0)
                            json.dump(data, fi)
                            fi.truncate()
                        break

            else:
                raise ErrorHandler.DeleteEntry(entries, self._table_name)

    def DeleteTable(self):

        if os.path.exists(f'./databases/{self._database_name}/{self._table_name}.fdb') and os.path.isfile(f'./databases/{self._database_name}/{self._table_name}.fdb'):
            os.remove(f'./databases/{self._database_name}/{self._table_name}.fdb')

        else:
            raise ErrorHandler.DeleteTable(self._database_name, self._table_name)

    def DeleteDatabase(self):

        if os.path.exists(f'./databases/{self._database_name}') and os.path.isdir(f'./databases/{self._database_name}'):
            os.rmdir(f'./databases/{self._database_name}')

        else:
            raise ErrorHandler.DeleteDatabase(self._database_name)
