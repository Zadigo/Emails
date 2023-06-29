from zemailer.core.senders import SendEmail
from zemailer.patterns import EmailGenerator

e = EmailGenerator('Kylie', 'Schuyler')
# e.to_file()
subject = 'Opportunité de partenariat'
body = """
Bonjour,

Je m'appelle Marie Dubois, une entrepreneure passionnée par le monde de la cuisine et de la gastronomie. Après avoir travaillé dans le domaine de la finance, j'ai décidé de suivre ma passion et de lancer mon entreprise, Keppler, spécialisée dans la vente d'équipements haut de gamme pour les professionnels de la cuisine à Lille.

Chez Keppler, nous comprenons l'importance d'avoir des outils de qualité supérieure pour créer des expériences culinaires exceptionnelles. C'est pourquoi nous nous sommes engagés à fournir à nos clients les meilleurs équipements de cuisine disponibles sur le marché.

Notre gamme de produits comprend une sélection minutieuse d'appareils électroménagers haut de gamme, d'ustensiles de cuisine de qualité professionnelle, de systèmes de cuisson innovants et bien plus encore. Nous travaillons en étroite collaboration avec les principales marques internationales pour vous offrir des produits de renom, reconnus pour leur fiabilité, leur durabilité et leurs performances exceptionnelles.

En tant que restaurateurs et chefs cuisiniers, vous savez à quel point les équipements de cuisine de qualité sont essentiels pour préparer des plats savoureux et impressionner vos clients. Chez Keppler, nous comprenons vos besoins spécifiques et nous sommes là pour vous fournir des solutions sur mesure, adaptées à votre établissement.

En choisissant Keppler, vous bénéficiez d'une expérience client personnalisée et d'un service exceptionnel. Notre équipe d'experts en équipements de cuisine est disponible pour vous conseiller et vous guider dans le choix des meilleurs produits pour répondre à vos besoins et à vos exigences spécifiques. Nous sommes là pour vous accompagner tout au long du processus, de la sélection des équipements à leur installation et à leur entretien.

De plus, notre partenariat avec les principales marques nous permet de vous offrir des prix compétitifs sans compromettre la qualité. Nous comprenons l'importance de gérer efficacement votre budget tout en investissant dans des équipements qui amélioreront votre efficacité opérationnelle et votre qualité de production.

En résumé, chez Keppler, nous sommes passionnés par la gastronomie et nous sommes déterminés à fournir aux professionnels de la cuisine des équipements haut de gamme qui répondent à leurs exigences les plus élevées. Contactez-nous dès aujourd'hui pour discuter de vos besoins en équipements de cuisine et laissez-nous vous aider à créer une cuisine d'exception pour votre établissement à Lille. Ensemble, nous pouvons faire de votre vision culinaire une réalité.
"""
# for email in e:
s = SendEmail('inglishgoogle.contact@gmail.com',
              'kylie.schuyler@california-bliss.fr', subject, email_body=body)
