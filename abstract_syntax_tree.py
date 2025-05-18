class Select:
    def __init__(self, columns, table, where=None, limit=None):
        self.columns = columns
        self.table = table
        self.where = where
        self.limit = limit

class Condition:
    def __init__(self, column, operator, value):
        self.column = column
        self.operator = operator
        self.value = value

class ImportTable:
    def __init__(self, table_name, file_path):
        self.table_name = table_name
        self.file_path = file_path

class ExportTable:
    def __init__(self, table_name, file_path):
        self.table_name = table_name
        self.file_path = file_path

class CreateTable:
    def __init__(self, new_table, table_1, table_2, column):
        self.new_table = new_table
        self.table_1 = table_1
        self.table_2 = table_2
        self.column = column

class CreateTableAsSelect:
    def __init__(self, new_table, select_query):
        self.new_table = new_table
        self.select_query = select_query

class DiscardTable:
    def __init__(self, table_name):
        self.table_name = table_name

class RenameTable:
    def __init__(self, old_name, new_name):
        self.old_name = old_name
        self.new_name = new_name

class PrintTable:
    def __init__(self, table_name):
        self.table_name = table_name

class Procedure:
    def __init__(self, name, commands):
        self.name = name
        self.commands = commands

class Call:
    def __init__(self, name):
        self.name = name