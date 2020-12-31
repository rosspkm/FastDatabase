import os


class FileExists(Exception):
    def __init__(self, name):
        super(FileExists, self).__init__(
            f'The File you are trying to create {name}.json already exists {os.path.abspath(name + ".fdb")}')


class DatabaseCreation(Exception):
    def __init__(self, database_name):
        super(DatabaseCreation, self).__init__(
            f'Can not create the Database you are trying to create {database_name}.fdb')


class LoadData(Exception):
    def __init__(self, database_name, table_name):
        super(LoadData, self).__init__(f'Was not able to load data from {database_name}/{table_name}.schema.fdb')


class SaveData(Exception):
    def __init__(self, name):
        super(SaveData, self).__init__(f'Was not able to save data to {name}.fdb')


class Type(Exception):
    def __init__(self, word, b):
        super(Type, self).__init__(f'Type Error "{word}" was supposed to be a(n) "{b}"')


class SelectTable(Exception):
    def __init__(self, database_name, table_name):
        super(SelectTable, self).__init__(f'Was unable to select table "{table_name}" from "{database_name}"')


class EmptyValue(Exception):
    def __init__(self, field, a, b):
        super(EmptyValue, self).__init__(f'Field "{field}" was empty and "{a}" was set to "{b}"')


class MinLength(Exception):
    def __init__(self, word, b):
        super(MinLength, self).__init__(f'"{word}" did not reach the minimum length of "{b}"')


class MaxLength(Exception):
    def __init__(self, word, b):
        super(MaxLength, self).__init__(f'"{word}" exceeded the maximum length set "{b}"')


class Duplicate(Exception):
    def __init__(self, content):
        super(Duplicate, self).__init__(f'"{content}" is a duplicate entry')


class InvalidField(Exception):
    def __init__(self, field):
        super(InvalidField, self).__init__(f'{field} was passed and was not a valid field')


class DeleteEntry(Exception):
    def __init__(self, entries, table_name):
        super(DeleteEntry, self).__init__(f'Could not delete "{entries}" from "{table_name}", maybe it does not exist')


class DeleteDatabase(Exception):
    def __init__(self, database_name):
        super(DeleteDatabase, self).__init__(f'Could not delete the database "{database_name}", maybe it does not exist')


class DeleteTable(Exception):
    def __init__(self, database_name, table_name):
        super(DeleteDatabase, self).__init__(f'Could not delete the table "{table_name}" from the database "{database_name}", maybe it does not exist')


class ShowTable(Exception):
    def __init__(self, database_name, table_name):
        super(ShowTable, self).__init__(f'Could not load data of table "{table_name}" from the database "{database_name}", maybe it does not exist')
