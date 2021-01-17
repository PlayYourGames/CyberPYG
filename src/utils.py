import json
import os


def retrieve_secret_data(key: str):
    """ Retrieve data from a key string """
    with open('config/env.json', 'r+') as file:
        data = json.load(file)
    return data[key]


def load_cogs(_client, subdir: str):
    """ Load subfolder cogs """
    for _cog in [file.split(".")[0] for file in os.listdir(f'cogs/{subdir}') if file.endswith('.py')]:
        subdir = subdir.replace('/', '.')
        try:
            _client.load_extension(f'cogs.{subdir}.{_cog}') if _cog != '__init__' else ...
        except Exception as e:
            print(e)
