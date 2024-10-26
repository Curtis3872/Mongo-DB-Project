from pprint import pformat
from pymongo.errors import OperationFailure
from mongoengine import *
import io
import certifi
from pymongo import MongoClient


class Utilities:
    @staticmethod
    def startup():
        while True:
            username: str = input("MongoDB Username: ")
            password: str = input("MongoDB Database Password: ")
            hash_name: str = input("DB hash: ")
            database_name: str = input("DB Name: ")
            cluster = f"mongodb+srv://{username}:{password}@{database_name}.{hash_name}.mongodb.net/?retryWrites=true&w=majority"
            cluster_censored = f"mongodb+srv://{username}:*******@cluster0.{hash_name}.mongodb.net/?retryWrites=true&w=majority"
            ca = certifi.where()
            client = connect(db=database_name,host=cluster,tlsCAFile=ca)
            try:
                print(f"Connected to {cluster_censored}")
                junk = client.server_info()
                return client
            except OperationFailure as OE:
                print(OE)
                print("Error, invalid password.  Try again.")

    @staticmethod
    def print_exception(thrown_exception: Exception):
        with io.StringIO() as output:
            output.write('***************** Start of Exception print *****************\n')
            output.write(f'The exception is of type: {type(thrown_exception).__name__}\n')
            if isinstance(thrown_exception, NotUniqueError):
                error = thrown_exception.args[0]
                message = error[error.index('index:') + 7:error.index('}')]
                index_name = message[:message.index(' ')]
                field_list = message[message.index('{') + 2:]
                fields = []
                while field_list.find(':') > 0:
                    field_length = field_list.find(':')
                    field = field_list[:field_length]
                    fields.append(field)
                    if (field_list.find(', ')) > 0:
                        field_list = field_list[field_list.find(', ') + 2:]
                    else:
                        field_list = ''
                output.write(f'Uniqueness constraint violated: {index_name} with fields:\n{fields}')
            elif isinstance(thrown_exception, ValidationError):
                output.write(f'{pformat(thrown_exception.message)}\n')
                errors = thrown_exception.errors
                for error in errors.keys():
                    output.write(f'field name: {error} has issue: \n{pformat(errors.get(error))}\n')
            results = output.getvalue().rstrip()
        return results
