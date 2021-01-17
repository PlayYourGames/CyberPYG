import json


def retrieve_secret_data(key: str):
    """ Retrieve data from a key string """
    with open('config/env.json', 'r+') as file:
        data = json.load(file)
    return data[key]
