from email_constructor import NamePatterns

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

print(ISCOM('test'))