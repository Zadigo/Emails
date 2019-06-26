"""This module regroups a series of classes that can be used
to construct emails off business schools.
"""

from email_app.patterns.patterns import NamePatterns
from email_app.mixins.fields import EmailField
import requests

class EDHEC(NamePatterns):
    pattern = 'nom.prenom'
    domain = ''

class HEC(NamePatterns):
    pattern = ['nomp', 'nom']
    domain = 'hec.fr'

class EMLyon(NamePatterns):
    pattern = 'nom.prenom'
    domain = 'em-lyon.com'

class SKEMA(NamePatterns):
    pattern = 'prenom.nom'
    domain = 'skema.edu'

class PolytechParis(NamePatterns):
    pattern = 'prenom.nom'
    domain = 'polytechnique.edu'

class ESCP(NamePatterns):
    pattern = 'pnom'
    domain = 'escpeurope.eu'

class CentraleParis(NamePatterns):
    pattern = 'nom.prenom'
    domain = ''

class CentraleLille(CentraleParis):
    domain = ''

class HEI(NamePatterns):
    pattern = 'nom.prenom'
    domain = ''

class KEDGE(NamePatterns):
    pattern = 'prenom.nom'
    domain = 'kedgebs.com'

class ISCOM(NamePatterns):
    pattern = 'prenom.nom'
    domain = 'iscom.fr'

class ESSEC(NamePatterns):
    pattern = ['nom', 'nomp']
    domain = 'essec.edu'

class Neoma(NamePatterns):
    pattern = 'prenom.nom'
    domain = 'neoma.fr'

class ISTC(NamePatterns):
    pattern = ''

class Universities(NamePatterns):
    """This class is voluntarily empty
    and can subclassed to create patterns
    for universities
    """
    def from_url(self, url):
        if self._ping(url):
            pass
        pass

    @staticmethod
    def _ping(url):
        response = requests.get(url, headers={'User-Agent': ''})
        if response.status_code == 200:
            return True
        return False
