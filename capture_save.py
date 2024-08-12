import csv
from csv import writer
import zipfile
from pylookyloo import Lookyloo
from uuids_fake import uuids_amendes, uuids_paypal, uuids_atandt, uuids_amazon, uuids_netflix, uuids_ameli, uuids_credit_agricole, uuids_microsoft, uuids_luxtrust,uuids_orange

lookyloo = Lookyloo()

if lookyloo.is_up:
    #name of the institution so that we do not have to change the paths in the code
    institution = "amazon"

    #need to change the uuid list manually
    for uuid in uuids_amazon:

        #saving the capture in the corresponding folder
        zip_buffer = lookyloo.get_complete_capture(uuid)
        print(uuid)

        with zipfile.ZipFile(zip_buffer, 'r') as zip_ref:
            zip_ref.extractall('./'+ institution +'_fake')
            name = zip_ref.namelist()[0].split('/')[0]
        zip_buffer.close()

        txt_datei = './'+ institution +'_fake/' + name + '/0.last_redirect.txt'

        csv_datei = './'+ institution +'_fake/'+ institution +'_urls.csv'

        #writing the uuid and the url into the csv file
        with open(txt_datei, 'r') as txt_file, open(csv_datei, 'a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([uuid])

            for zeile in txt_file:
                daten = zeile.strip().split(',')
                csv_writer.writerow(daten)

        csv_datei = './'+ institution +'_fake/'+ institution +'_takedown_info.csv'

        #takedown information are written into the csv file
        with open(csv_datei, 'a') as f_object:
            writer_object = writer(f_object)
            writer_object.writerow([uuid])
            writer_object.writerow(lookyloo.get_takedown_information(uuid))
            f_object.close()

