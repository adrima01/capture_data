import os
from bs4 import BeautifulSoup
import hashlib
from pylookyloo import Lookyloo
from csv import writer


"""companies = ["amazon", "ameli", "amendes", "atandt", "credit_agricole", "luxtrust", "microsoft", "netflix", "orange", "paypal"]
#companies = ["credit_agricole"]
count = 0
for company in companies:
    for root, dirs, files in os.walk("../" + company + "_legitimate"):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            uuid_path = dir_path + "/uuid"
            with open(uuid_path, 'r') as file:
                uuid = file.readline().strip()
            print(uuid)
print(count)

for company in companies:
    print(company)
    #did the fake ones with the public instance
    #go through every directory
    for root, dirs, files in os.walk("../" + company + "_fake"): #first all the fakes
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            print(dir_path)


https://www.credit-agricole.fr/particulier/assurances/auto-2-roues/assurance-scooter.html
https://www.credit-agricole.fr/particulier/simulation-devis.html
https://www.credit-agricole.fr/particulier/epargne/retraite/per-compte-titres.html
https://www.credit-agricole.fr/particulier/assurances/auto-2-roues/assurance-jeune-conducteur.html
https://www.credit-agricole.fr/particulier/assurances/loisir-quotidien/assurance-tous-mobiles.html
https://www.credit-agricole.fr/particulier/compte/carte-bancaire/carte-mozaic-black-as.html
https://www.credit-agricole.fr/particulier/compte/service-bancaire/offre-premium.html
https://www.credit-agricole.fr/professionnel.html
https://www.credit-agricole.fr/particulier/credit/immobilier.html
https://www.credit-agricole.fr/particulier/epargne/investissement-socialement-responsable/amundi-france-engagement.html
https://www.credit-agricole.fr/particulier/credit/travaux/pret-a-consommer-confort.html
https://www.credit-agricole.fr/particulier/compte/service-bancaire/eko.html
https://www.credit-agricole.fr/particulier/compte/carte-bancaire/carte-visa-premier-debit-differe.html
https://www.credit-agricole.fr/particulier/compte/paiement-mobile/apple-pay.html
https://www.credit-agricole.fr/particulier/compte/carte-bancaire.html
https://www.credit-agricole.fr/particulier/conseils/retraite/bien-vivre-ma-retraite.html
https://www.credit-agricole.fr/particulier/assurances/credit/assurance_emprunteur_credit_immobilier.html
https://www.credit-agricole.fr/particulier/informations/tarifs.html
https://www.credit-agricole.fr/particulier/informations/banque-cooperative.html
https://www.credit-agricole.fr/particulier/epargne/livret-epargne-logement/livret-d-epargne-populaire-lep.html
https://www.credit-agricole.fr/particulier/epargne/livret-epargne-logement/livret-a.html
https://www.credit-agricole.fr/particulier/conseils/coups-durs/maitriser-votre-budget.html
https://www.credit-agricole.fr/particulier/compte/service-bancaire/globe-trotter.html
https://www.credit-agricole.fr/particulier/conseils/coups-durs/mes-coups-durs.html
https://www.credit-agricole.fr/particulier/informations/mentions-legales.html
https://www.credit-agricole.fr/particulier/conseils/mon-vehicule/vehicule.html
https://www.credit-agricole.fr/particulier/assurances.html
https://www.credit-agricole.fr/particulier/caisses-regionales.html
https://www.credit-agricole.fr/particulier/compte/paiement-mobile/samsung-pay.html
https://www.credit-agricole.fr/particulier/informations/reclamation-mediation.html
https://www.credit-agricole.fr/particulier/assurances/loisir-quotidien/assurance-responsabilite-civile-vie-privee.html
https://www.credit-agricole.fr/particulier/epargne/investissement-socialement-responsable/l-investissement-responsable.html
https://www.credit-agricole.fr/particulier/conseils/patrimoine/diversifier.html
https://www.credit-agricole.fr/particulier/epargne/livret-epargne-logement/livret-societaires.html
https://www.credit-agricole.fr/particulier/cybersecurite.html
https://www.credit-agricole.fr/particulier/acces-cr-et-agence.html?origin=/content/ca/national/npc/fr/particulier/compte/carte-bancaire/carte-mastercard-standard-debit-differe.html
https://www.credit-agricole.fr/particulier/credit/travaux.html
https://www.credit-agricole.fr/particulier/assurances/credit.html
https://www.credit-agricole.fr/particulier/informations/relation-banque-client.html
https://www.credit-agricole.fr/particulier/assurances/habitation/telesurveillance.html
https://www.credit-agricole.fr/particulier/credit/vehicule/pret-2-roues.html
https://www.credit-agricole.fr/particulier/credit/consommation/credit-renouvelable.html
https://www.credit-agricole.fr/particulier/conseils/logement/financer.html
https://www.credit-agricole.fr/particulier/assurances/auto-2-roues/assurance-auto.html
https://www.credit-agricole.fr/particulier/compte/magazine/sante-magazine.html
https://www.credit-agricole.fr/particulier/epargne/retraite.html
https://www.credit-agricole.fr/association.html
https://www.credit-agricole.fr/particulier/simulation-devis/comptes-et-cartes/choisir-offre-bancaire.html
https://www.credit-agricole.fr/particulier/conseils/patrimoine/gerer.html
https://www.credit-agricole.fr/agriculteur.html
https://www.credit-agricole.fr/particulier/credit/travaux/pret-transition-logement.html
https://www.credit-agricole.fr/particulier/informations/fgdr.html
https://www.credit-agricole.fr/particulier/accessibilite.html
https://www.credit-agricole.fr/particulier/compte/paiement-mobile.html
https://www.credit-agricole.fr/particulier/epargne/assurance-vie/floriane.html
https://www.credit-agricole.fr/particulier/compte.html
https://www.credit-agricole.fr/particulier/epargne/investissement-socialement-responsable.html
https://www.credit-agricole.fr/particulier/informations/notre-projet-societal.html
https://www.credit-agricole.fr/particulier/conseils/logement/rechercher.html
https://www.credit-agricole.fr/particulier/epargne/assurance-vie/l-assurance-vie.html
https://www.credit-agricole.fr/particulier/assurances/habitation/assurance-habitation-formule-jeune.html"""

import csv
from csv import writer
import zipfile
from pylookyloo import Lookyloo
from uuids_legitimate import uuids_amazon, uuids_ameli, uuids_amendes, uuids_atandt, uuids_credit_agricole, \
    uuids_luxtrust, uuids_microsoft, uuids_netflix, uuids_orange, uuids_paypal, other

lookyloo = Lookyloo()

if lookyloo.is_up:
    #name of the institution so that we do not have to change the paths in the code
    institution = "other_test"

    #need to change the uuid list manually
    for uuid in other:

        #saving the capture in the corresponding folder
        zip_buffer = lookyloo.get_complete_capture(uuid)
        #print(uuid)

        with zipfile.ZipFile(zip_buffer, 'r') as zip_ref:
            #zip_ref.extractall('./'+ institution +'_legitimate')
            zip_ref.extractall('./'+ institution)
            name = zip_ref.namelist()[0].split('/')[0]
        zip_buffer.close()

        #txt_datei = './'+ institution +'_legitimate/' + name + '/0.last_redirect.txt'
        txt_datei = institution +'/' + name + '/0.last_redirect.txt'
        html_datei = institution +'/' + name + '/0.html'

        if not os.path.exists(txt_datei) or not os.path.exists(html_datei):
            print(uuid)







