import csv
import os

from app.core.conf._settings import initialized_settings
from app.core.messages import Info


def converter(filename):
    path = os.path.join(initialized_settings.get('settings__data_path'), filename)
    file_to_write = os.path.join(initialized_settings.get('settings__data_path'), 'test.csv')

    if not os.path.exists(path):
        return Info('The file doest not exist.')

    with open(path, 'r', encoding='utf-8') as f:
        with open(file_to_write, 'r+', encoding='utf-8') as c:
            names = []
            lines = f.readlines()
            for line in lines:
                name = str(line).split(' ')

                s = csv.writer(c)
                s.writerow(name)
