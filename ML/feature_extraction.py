import ast
import csv
import os
from urllib.parse import urlparse

from bs4 import BeautifulSoup
import hashlib
from pylookyloo import Lookyloo
from csv import writer

companies = ["amazon", "ameli", "amendes", "atandt", "credit_agricole", "luxtrust", "microsoft", "netflix", "orange", "paypal"]


def write_files(name, features, label):
    file_name = "datasets/"+ name + "_dataset.csv"
    features_copy = features.copy()
    features_copy.append(label)
    with open(file_name, 'a') as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(features_copy)
        f_object.close()

def read_uuid(path):
    uuid_path= path + "/uuid"
    with open(uuid_path, 'r') as file:
        uuid = file.readline().strip()
    return uuid

def get_variations_list(company):
    path = "typosquatting_lists/" + company + "_variations.txt"
    with open(path, 'r') as file:
        list = file.read()
    return list

def check_list(list, path):
    domain = get_domain(path)
    return "1" if domain in list else "0"

def get_3rd_party_responses(uuid):
        response = lookyloo.get_modules_responses(uuid)
        if not response:
            return None
        modules = set()
        if 'vt' in response:
            vt = response.pop('vt')
            for url, report in vt.items():
                if not report:
                    continue
                for vendor, result in report['attributes']['last_analysis_results'].items():
                    if result['category'] == 'malicious':
                        modules.add(vendor)

        if 'pi' in response:
            pi = response.pop('pi')
            for url, full_report in pi.items():
                if not full_report:
                    continue
                modules.add('Phishing Initiative')

        if 'phishtank' in response:
            pt = response.pop('phishtank')
            for url, full_report in pt['urls'].items():
                if not full_report:
                    continue
                modules.add('Phishtank')

        if 'urlhaus' in response:
            uh = response.pop('urlhaus')
            for url, results in uh['urls'].items():
                if results:
                    modules.add('URLhaus')

        if 'urlscan' in response and response.get('urlscan'):
            urlscan = response.pop('urlscan')
            if 'error' not in urlscan['submission']:
                if urlscan['submission'] and urlscan['submission'].get('result'):
                    if urlscan['result']:
                        if (urlscan['result'].get('verdicts')
                                and urlscan['result']['verdicts'].get('overall')):
                            if urlscan['result']['verdicts']['overall'].get('malicious'):
                                modules.add('urlscan')
                else:
                    # unable to run the query, probably an invalid key
                    pass
        if len(modules) == 0:
            return "0"
        return len(modules)

def getthis(path):
    html_path = path + "/0.html"
    with open(path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, 'html.parser')#?????????????????????????????????????


def get_domain(path):
    last_redirect_path= path + "/0.last_redirect.txt"
    with open(last_redirect_path, 'r') as file:
        url = file.readline().strip()
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    return domain

def get_takedown_info(company, nature, uuid):
    takedown_path = "../" + company + "_" + nature + "/" + company + "_takedown_info.csv"
    with open(takedown_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        rows = list(reader)

        for i in range(0, len(rows), 2):
            uuid_row = rows[i]
            info_row = rows[i + 1] if i + 1 < len(rows) else None

            if uuid_row and len(uuid_row) > 0 and uuid_row[0] == uuid:
                if info_row and len(info_row) > 0:
                    try:
                        info_dict = ast.literal_eval(info_row[0])
                        return info_dict
                    except (ValueError, SyntaxError) as e:
                        print("Error")
                        return None

    return None

lookyloo = Lookyloo()


if lookyloo.is_up:
    for company in companies:
        print(company)
        typosquatting = get_variations_list(company)
        #did the fake ones with the public instance
        #go through every directory
        for root, dirs, files in os.walk("../" + company + "_fake"): #first all the fakes
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                print(dir_path)
                uuid = read_uuid(dir_path)
                features = []

                #1 when the hostname is contained in the typosquatting list
                features.append(check_list(typosquatting, dir_path))

                #getting the number of how often the url was found in other phishing databases
                features.append(get_3rd_party_responses(uuid))

                #getting the domain length
                features.append(len(get_domain(dir_path)))

                #host based features
                takedown_info = get_takedown_info(company, "fake", uuid) #dict with takedown information



                features.append("1") #1 means that it is a fake website


                for company_dataset in companies:
                    if company_dataset == company:
                        label = "1" #1 so that it is marked as the company we are training the dataset on
                    else:
                        label = "0"
                    write_files(company_dataset, features, label)












        #did the legitimate ones with demo and public instance
        for root, dirs, files in os.walk("../" + company + "_legitimate"):
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                print(dir_path)
                uuid = read_uuid(dir_path)

                features = []

                #1 when the hostname is contained in the typosquatting list
                features.append(check_list(typosquatting, uuid))

                #getting the number of how often the url was found in other phishing databases
                features.append(get_3rd_party_responses(uuid))

                features.append("1") #1 means that it is a fake website

                for company_dataset in companies:
                    if company_dataset == company:
                        label = "1" #1 so that it is marked as the company we are training the dataset on
                    else:
                        label = "0"
                    write_files(company_dataset, features, label)
