import ast
import csv
import os
import geocoder
from urllib.parse import urlparse
from similarius import get_website, extract_text_ressource, sk_similarity, ressource_difference, ratio
from ip2geotools.databases.noncommercial import DbIpCity


from bs4 import BeautifulSoup
import hashlib

from imagedominantcolor import DominantColor
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

def html_information(path, company):
    html_path = path + "/0.html"
    with open(html_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    name_presence = "1" if company in soup.get_text().lower() else "0"
    form_presence = "1" if soup.find('input') else "0"
    links = soup.find_all('a')
    number_links = len(links)
    empty_links = [link for link in links if link.get('href') == '#']
    domain = get_domain(path)
    domain_links = 0
    hrefs = [tag.get('href') for tag in soup.find_all(href=True)]
    for href in hrefs:
        if domain in href:
            domain_links += 1
    return name_presence, form_presence, number_links, len(empty_links), domain_links


def get_domain(path):
    last_redirect_path= path + "/0.last_redirect.txt"
    with open(last_redirect_path, 'r') as file:
        url = file.readline().strip()
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    return domain

def get_takedown_info(company, nature, uuid):
    takedown_path = "../" + company + "_" + nature + "/" + company + "_takedown_info.csv"
    if os.path.exists(takedown_path):
        with open(takedown_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            rows = list(reader)

            for i in range(0, len(rows), 2):
                uuid_row = rows[i]
                info_row = rows[i + 1] if i + 1 < len(rows) else None

                if uuid_row and len(uuid_row) > 0 and uuid_row[0] == uuid:
                    if info_row and len(info_row) > 0:
                        try:
                            dict_list = [ast.literal_eval(item) for item in info_row]

                            return dict_list

                        except (ValueError, SyntaxError) as e:
                            print("Error:", e)
    return None

def get_ips(info, path):
    domain = get_domain(path)
    for redirect in info:
        if redirect['hostname'] == domain:
            return list(redirect['ips'].keys())
    return None

#getting only the first ip
def get_geolocation(ips_list):
    """geo = geocoder.ip(ips_list[0])
    lat, long = geo.latlng[0], geo.latlng[1]"""

    response = DbIpCity.get(ips_list[0], api_key='free')
    return response.latitude, response.longitude

def dominant_color(path, type):
    if type == "screenshot":
        file_path = path + "/0.png"
    elif type == "favicon":
        file_path = path + "/0.potential_favicons.ico"
    if os.path.exists(file_path):
        dominantcolor = DominantColor(file_path)
        return dominantcolor.r, dominantcolor.g, dominantcolor.b
    return 0,0,0

def calculate_file_hash(file_path, hash_algorithm='sha256'):
    # Unterstützte Hash-Algorithmen
    hash_func = getattr(hashlib, hash_algorithm)()

    # Datei im Binärmodus lesen und den Hash berechnen
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_func.update(chunk)

        # Hexadezimale Darstellung des Hashs zurückgeben
        return int(hash_func.hexdigest(),16)
    return 0

def similarius_values(company, path):
    with open(company, 'r', encoding='utf-8') as file:
        html_content1 = file.read()
    soup1 = BeautifulSoup(html_content1, 'html.parser')


    original_text, original_ressource = extract_text_ressource(soup1.text)

    # Compare

    html_path = path + "/0.html"
    with open(html_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    compare_text, compare_ressource = extract_text_ressource(soup.text)

    # Calculate
    sim = str(sk_similarity(compare_text, original_text))

    return sim


lookyloo = Lookyloo()


if lookyloo.is_up:
    for company in companies:
        file_name = "datasets/" + company + "_dataset.csv"
        feature_list = ["uuid",
                        "dir_path",
                        "typosquatting_list",
                        "3rd_party_hits",
                        "domain_length",
                        "name_presence",
                        "form_presence",
                        "number_links",
                        "number_empty_links",
                        "number_links_domain",
                        "latitude",
                        "longitude",
                        "red_value_screenshot",
                        "green_value_screenshot",
                        "blue_value_screenshot",
                        "red_value_favicon",
                        "green_value_favicon",
                        "blue_value_favicon",
                        "hash_screenshot",
                        "hash_favicon",
                        "similarius_sim",
                        "malicious",
                        "company_site"]
        compare_sites= {
            "amazon": "/home/amaraj/Bachelorarbeit/capture_saver/amazon_legitimate/2024-08-21T12:17:23.058173/0.html",
            "ameli":"/home/amaraj/Bachelorarbeit/capture_saver/ameli_legitimate/2024-08-26T12:17:33.189636/0.html",
            "amendes":"/home/amaraj/Bachelorarbeit/capture_saver/amendes_legitimate/2024-08-21T14:44:09.691940/0.html",
            "atandt":"/home/amaraj/Bachelorarbeit/capture_saver/atandt_legitimate/2024-08-26T12:29:05.942666/0.html",
            "credit_agricole":"/home/amaraj/Bachelorarbeit/capture_saver/credit_agricole_legitimate/2024-08-21T14:30:17.582262/0.html",
            "luxtrust":"/home/amaraj/Bachelorarbeit/capture_saver/luxtrust_legitimate/2024-08-26T13:45:53.974198/0.html",
            "microsoft":"/home/amaraj/Bachelorarbeit/capture_saver/microsoft_legitimate/2024-08-21T14:20:58.145717/0.html",
            "netflix":"/home/amaraj/Bachelorarbeit/capture_saver/netflix_legitimate/2024-08-21T14:19:05.483055/0.html",
            "orange":"/home/amaraj/Bachelorarbeit/capture_saver/orange_legitimate/2024-08-21T13:47:47.622005/0.html",
            "paypal":"/home/amaraj/Bachelorarbeit/capture_saver/paypal_legitimate/2024-08-21T13:36:34.243552/0.html"
        }
        with open(file_name, 'a') as f_object:
            writer_object = writer(f_object)
            writer_object.writerow(feature_list)
            f_object.close()
    for company in companies:
        print(company)
        typosquatting = get_variations_list(company)
        #did the fake ones with the public instance
        #go through every directory
        for root, dirs, files in os.walk("../" + company + "_fake"): #first all the fakes
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                print(dir_path)
                features = []

                uuid = read_uuid(dir_path)

                #adding features

                #adding uuid and path
                features.append(uuid)
                features.append(dir_path)
                #1 when the hostname is contained in the typosquatting list
                features.append(check_list(typosquatting, dir_path))
                #getting the number of how often the url was found in other phishing databases
                features.append(get_3rd_party_responses(uuid))
                #getting the domain length
                features.append(len(get_domain(dir_path)))
                # form presence
                name_presence,form_presence, number_links, empty_links, domain_links = html_information(dir_path, company)
                features.append(name_presence)
                features.append(form_presence)
                features.append(number_links)
                features.append(empty_links)
                features.append(domain_links)
                #adding latitude and longitude
                takedown_infos = get_takedown_info(company, "fake", uuid)  # dict with takedown information
                ips = get_ips(takedown_infos, dir_path)
                latitude, longitude = get_geolocation(ips)
                features.append(latitude)
                features.append(longitude)
                #adding r,g,b values of dominant color of the screenshot and favicon
                r_screenshot, g_screenshot, b_screenshot = dominant_color(dir_path,"screenshot")
                features.append(r_screenshot)
                features.append(g_screenshot)
                features.append(b_screenshot)
                r_favicon, g_favicon, b_favicon = dominant_color(dir_path,"favicon")
                features.append(r_favicon)
                features.append(g_favicon)
                features.append(b_favicon)
                #hashes
                features.append(calculate_file_hash(dir_path + '/0.png', hash_algorithm='sha256'))
                features.append(calculate_file_hash(dir_path + '/0.potential_favicons.ico', hash_algorithm='sha256'))
                #similarius
                sim_value= similarius_values(compare_sites[company],dir_path)
                features.append(sim_value)
                #features.append(diff_value)
                #features.append(ratio_value)


                #print(takedown_info)
                #print(get_ips(takedown_info, dir_path))



                features.append("1") #1 means that it is a fake website


                for company_dataset in companies:
                    if company_dataset == company:
                        label = "1" #1 so that it is marked as the company we are training the dataset on
                    else:
                        label = "0"
                    write_files(company_dataset, features, label)












        """"#did the legitimate ones with demo and public instance
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
                    write_files(company_dataset, features, label)"""