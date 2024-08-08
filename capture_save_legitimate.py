import csv
import time
import re
from csv import writer
import zipfile

from bs4 import BeautifulSoup
from pylookyloo import Lookyloo
from uuids_legitimate import uuids_netlfix

def finding_links(path: str) -> set:
    soup = BeautifulSoup(path, "html.parser")
    hrefs = {link.get("href") for link in soup.find_all("a")}
    return hrefs

lookyloo = Lookyloo("http://0.0.0.0:5100/")

if lookyloo.is_up:
    #name of the institution so that we do not have to change the paths in the code
    institution = "amendes"

    url = input("Enter an URL: ")
    uuid = lookyloo.submit(url=url, quiet=True)
    while lookyloo.get_status(uuid)['status_code'] != 1:
        time.sleep(1)

    csv_file = institution + '_uuids.csv'
    with open(csv_file, 'a') as f_object:
        writer_object = writer(f_object)
        writer_object.writerow([institution])
        writer_object.writerow([uuid])


    html = lookyloo.get_html(uuid).read()
    hrefs = finding_links(html)
    hostname = lookyloo.get_info(uuid)['url']
    count = 0
    for href in hrefs:
        if isinstance(href, str) and re.match("^/", href):
            # putting together the url
            new_url = hostname + href
            new_uuid = lookyloo.submit(url=new_url, quiet=True)
            count += 1
            with open(csv_file, 'a') as f_object:
                writer_object = writer(f_object)
                writer_object.writerow([new_uuid])

    print(f"{count} capture(s) ongoing")

    #need to change the uuid list manually
    """for uuid in uuids_netlfix:

        #saving the capture in the corresponding folder
        zip_buffer = lookyloo.get_complete_capture(uuid)
        print(uuid)

        with zipfile.ZipFile(zip_buffer, 'r') as zip_ref:
            zip_ref.extractall('./'+ institution +'_legitimate')
            name = zip_ref.namelist()[0].split('/')[0]
        zip_buffer.close()

        txt_datei = './'+ institution +'_legitimate/' + name + '/0.last_redirect.txt'

        csv_datei = './'+ institution +'_legitimate/'+ institution +'_urls.csv'

        #writing the uuid and the url into the csv file
        with open(txt_datei, 'r') as txt_file, open(csv_datei, 'a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([uuid])

            for zeile in txt_file:
                daten = zeile.strip().split(',')
                csv_writer.writerow(daten)

        csv_datei = './'+ institution +'_legitimate/'+ institution +'_takedown_info.csv'

        #takedown information are written into the csv file
        with open(csv_datei, 'a') as f_object:
            writer_object = writer(f_object)
            writer_object.writerow([uuid])
            writer_object.writerow(lookyloo.get_takedown_information(uuid))
            f_object.close()"""

