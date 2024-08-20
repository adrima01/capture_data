import csv
from csv import writer
import zipfile
from pylookyloo import Lookyloo
from uuids_legitimate import uuids_amazon, uuids_ameli, uuids_amendes, uuids_atandt, uuids_credit_agricole, \
    uuids_luxtrust, uuids_microsoft, uuids_netflix, uuids_orange, uuids_paypal

lookyloo = Lookyloo("https://lookyloo-demo.yoyodyne-it.eu/")

if lookyloo.is_up:
    #name of the institution so that we do not have to change the paths in the code
    institution = "paypal"

    #need to change the uuid list manually
    for uuid in uuids_paypal:

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
            f_object.close()