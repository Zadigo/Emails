import os
from zemailer.settings import configuration
from zemailer.utils.module_loader import import_module
from functools import cached_property, lru_cache


# @cached_property
def collect_commands():
    current_path = os.path.dirname(os.path.abspath(__file__))
    commands_path = os.path.join(current_path, 'commands')
    _, _, files = list(os.walk(commands_path))[0]
    for item in files:
        name, _ = item.split('.')
        yield f'zemailer.management.commands.{name}'
    # return list(map(lambda x: os.path.join(root, x), files))



def load_commands():
    for dotted_path in collect_commands():
        yield import_module(dotted_path)


class CommandsRegistry:
    MODULE = None
    
    def __init__(self, module):
        pass


class Utility:
    def __init__(self, arguments):
        pass


print(list(load_commands()))
