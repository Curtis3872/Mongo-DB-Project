from datetime import datetime
from Menu import Menu
from Option import Option

def prompt_for_date(prompt: str) -> datetime:
    print(prompt)
    valid = False
    while not valid:
        try:
            year: int = int(input('Enter year --> '))
            month: int = int(input('Enter month number --> '))
            day: int = int(input('Enter day number --> '))
            hour: int = int(input('Enter hour (24 hour clock) --> '))
            minute: int = int(input('Enter minute number --> '))
            second: int = int(input('Enter second number --> '))
            timestamp = datetime.datetime(year, month, day, hour, minute, second)
            return timestamp
        except ValueError as ve:
            print('Error on input: ', ve)
            print('Please try again.')

def get_attr_from_column(cls, column_name) -> str:
    for attribute in cls.__dict__['_fields'].keys():
        if getattr(cls, attribute).__dict__['db_field'] == column_name:
            return attribute
def select_general(cls):
    collection = cls._get_collection()
    index_info = collection.index_information()
    choices = []
    for index in index_info.keys():
        if index == '_id_' or index_info[index]['unique']:
            columns = [col[0] for col in index_info[index]['key']]
            choices.append(Option(f'index: {index} - cols: {columns}', index))
    index_menu = Menu('which index', 'Which index do you want to search by:', choices)
    while True:
        chosen_index = index_menu.menu_prompt()
        filters = {}
        for column in [col[0] for col in index_info[chosen_index]['key']]:
            attribute_name = get_attr_from_column(cls, column)
            attribute = getattr(cls, attribute_name)
            if type(attribute).__name__ == 'ReferenceField':
                referenced_class = attribute.document_type
                target = select_general(referenced_class)
                filters[attribute_name] = target
            elif type(attribute).__name__ == 'DateTimeField':
                filters[attribute_name] = prompt_for_date(f'search for {attribute_name} =:')
            else:
                filters[attribute_name] = input(f'search for {attribute_name} = --> ')
        if cls.objects(**filters).count() == 1:
            return cls.objects(**filters).first()
        else:
            print('Sorry, no rows found that match those criteria.  Try again.')

def unique_general(instance):
    cls = instance.__class__
    collection = cls._get_collection()
    index_info = collection.index_information()
    constraints = []
    violated_constraints = []
    for index in index_info.keys():
        if index == '_id_' or index_info[index]['unique']:
            columns = [col[0] for col in index_info[index]['key']]
            constraints.append({'name': index, 'columns': columns})
    for constraint in constraints:
        filters = {}
        for column in constraint['columns']:
            attribute_name = get_attr_from_column(cls, column)
            filters[attribute_name] = instance[attribute_name]
        if cls.objects(**filters).count() == 1:
            violated_constraints.append(constraint)
    return violated_constraints