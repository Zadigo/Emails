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

John PENDENQUE - pendenquejohn@gmail.com
"""

import re
from urllib.parse import urlparse

import requests

# from zemailer.core.mixins.fields import EmailField
from zemailer.patterns.algorithms import Names


class EDHEC(Names):
    pattern = 'nom.prenom'
    domain = ''


class HEC(Names):
    pattern = ['nomp', 'nom']
    domain = 'hec.fr'


class EMLyon(Names):
    pattern = 'nom.prenom'
    domain = 'em-lyon.com'


class SKEMA(Names):
    pattern = 'prenom.nom'
    domain = 'skema.edu'


class PolytechParis(Names):
    pattern = 'prenom.nom'
    domain = 'polytechnique.edu'


class ESCP(Names):
    pattern = 'pnom'
    domain = 'escpeurope.eu'


class CentraleParis(Names):
    pattern = 'nom.prenom'
    domain = ''


class CentraleLille(CentraleParis):
    domain = ''


class HEI(Names):
    pattern = 'nom.prenom'
    domain = ''


class KEDGE(Names):
    pattern = 'prenom.nom'
    domain = 'kedgebs.com'


class ISCOM(Names):
    pattern = 'prenom.nom'
    domain = 'iscom.fr'


class ESSEC(Names):
    pattern = ['nom', 'nomp']
    domain = 'essec.edu'


class Neoma(Names):
    pattern = 'prenom.nom'
    domain = 'neoma.fr'


class ISTC(Names):
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
