from email_constructor import EmailPatterns

class EDHEC(EmailPatterns):
    pattern = 'nom.prenom'
    domain = ''

class HEC(EmailPatterns):
    pattern = ['nomp', 'nom']
    domain = 'hec.fr'

class EMLyon(EmailPatterns):
    pattern = 'nom.prenom'
    domain = 'em-lyon.com'

class SKEMA(EmailPatterns):
    pattern = 'prenom.nom'
    domain = 'skema.edu'

class PolytechParis(EmailPatterns):
    pattern = 'prenom.nom'
    domain = 'polytechnique.edu'

class ESCP(EmailPatterns):
    pattern = 'pnom'
    domain = 'escpeurope.eu'

class CentraleParis(EmailPatterns):
    pattern = 'nom.prenom'
    domain = ''

class CentraleLille(CentraleParis):
    domain = ''

class HEI(EmailPatterns):
    pattern = 'nom.prenom'
    domain = ''

class KEDGE(EmailPatterns):
    pattern = 'prenom.nom'
    domain = 'kedgebs.com'

class ISCOM(EmailPatterns):
    pattern = 'prenom.nom'
    domain = 'iscom.fr'

class ESSEC(EmailPatterns):
    pattern = ['nom', 'nomp']
    domain = 'essec.edu'

print(SKEMA('path').construct_pattern())