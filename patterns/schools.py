"""
This module regroups a series of preset
patterns related to schools in order to quickly
create a series of patterns.

Description
-----------

You can either subclass an already defined school or
create a new school by subclass Names.

For instance, improving a school would look like this:

    class EDHEC2(EDHEC):
        pattern = ''
        domain = ''

By calling EDHEC2(), you would create then a list of emails
from the pattern and domain that you would have provided.

Creating a new school is very simple:

    class NewSchool(NamePattenrs):
        pattern = ''
        domain = ''
"""

import re
from urllib.parse import urlparse

import requests
from zemailer.patterns.algorithms import NamesMixin


class EDHEC(NamesMixin):
    # pattern = 'nom.prenom'
    pattern = 'surname.name'
    domain = ''

class HEC(NamesMixin):
    # pattern = ['nomp', 'nom']
    pattern = ['surnamen', 'surname']
    domain = 'hec.fr'
    

class EMLyon(NamesMixin):
    # pattern = 'nom.prenom'
    pattern = 'surname.name'
    domain = 'em-lyon.com'


class SKEMA(NamesMixin):
    # pattern = 'prenom.nom'
    pattern = 'surname.name'
    domain = 'skema.edu'


class PolytechParis(NamesMixin):
    # pattern = 'prenom.nom'
    pattern = 'name.surname'
    domain = 'polytechnique.edu'


class ESCP(NamesMixin):
    # pattern = 'pnom'
    pattern = 'nsurname'
    domain = 'escpeurope.eu'


class CentraleParis(NamesMixin):
    # pattern = 'nom.prenom'
    pattern = 'surname.name'
    domain = ''


class CentraleLille(CentraleParis):
    domain = ''


class HEI(NamesMixin):
    # pattern = 'nom.prenom'
    pattern = 'surname.name'
    domain = ''


class KEDGE(NamesMixin):
    # pattern = 'prenom.nom'
    pattern = 'surname.name'
    domain = 'kedgebs.com'


class ISCOM(NamesMixin):
    # pattern = 'prenom.nom'
    pattern = 'surname.name'
    domain = 'iscom.fr'


class ESSEC(NamesMixin):
    pattern = ['nom', 'nomp']
    domain = 'essec.edu'


class Neoma(NamesMixin):
    # pattern = 'prenom.nom'
    pattern = 'surname.name'
    domain = 'neoma.fr'


class ISTC(NamesMixin):
    pattern = ''
    domain = ''


# class Universities(Names):
#     """This class is voluntarily empty
#     and can be subclassed to create patterns
#     for universities
#     """
#     def from_url(self, url):
#         if self._ping(url):
#             parsed_url = urlparse(url)[1]
#             domain = re.match(r'www\.(\S+)\.\w+', parsed_url)
#             if domain:
#                 structured_domain = f'@{domain}' % domain.group(1)
#                 return structured_domain
#             else:
#                 print('[INFO] Could not parse domain from url: %s' % url)
#                 return
#         else:
#             raise requests.exceptions.InvalidURL()

#     @staticmethod
#     def _ping(url):
#         response = requests.get(url, headers={'User-Agent': ''})
#         if response.status_code == 200:
#             return True
#         return False
