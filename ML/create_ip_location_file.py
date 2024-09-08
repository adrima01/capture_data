import ast
import csv
import os
from urllib.parse import urlparse

import requests
from csv import writer




def get_takedown_info(company, nature, uuid):
    if nature:
        takedown_path = "../" + company + "_" + nature + "/" + company + "_takedown_info.csv"
    else:
        takedown_path = "../other/other_takedown_info.csv"
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

def get_domain(path):
    last_redirect_path= path + "/0.last_redirect.txt"
    with open(last_redirect_path, 'r') as file:
        url = file.readline().strip()
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    return domain


def get_ips(info, path):
    domain = get_domain(path)
    for redirect in info:
        if redirect['hostname'] == domain:
            return list(redirect['ips'].keys())
    return None
def read_uuid(path):
    uuid_path= path + "/uuid"
    with open(uuid_path, 'r') as file:
        uuid = file.readline().strip()
    return uuid


companies = ["amazon", "ameli", "amendes", "atandt", "credit_agricole", "luxtrust", "microsoft", "netflix", "orange", "paypal"]

for company in companies:
       print(company)

       for root, dirs, files in os.walk("../" + company + "_legitimate"):  # first all the fakes
           for dir_name in dirs:
               dir_path = os.path.join(root, dir_name)
               print(dir_path)
               uuid = read_uuid(dir_path)
               takedown_information = get_takedown_info(company, "legitimate", uuid)
               ips = get_ips(takedown_information, dir_path)

               file_name = "ips_list/" + company + "_ips.csv"

               with open(file_name, 'a') as f_object:
                   writer_object = writer(f_object)
                   for ip in ips:
                       ip = [str(ip)]  # Wandle die IP-Adresse in eine Liste mit einem einzelnen Element um
                       writer_object.writerow(ip)
                   f_object.close()