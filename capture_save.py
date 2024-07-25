import csv
from csv import writer
import zipfile
from pylookyloo import Lookyloo
from uuids_fake import uuids_amendes, uuids_paypal,uuids_atandt, uuids_ameli, uuids_microsoft, uuids_luxtrust

lookyloo = Lookyloo()

if lookyloo.is_up:
    institution = "microsoft"

    for uuid in uuids_microsoft:

        zip_buffer = lookyloo.get_complete_capture(uuid)
        print(uuid)

        with zipfile.ZipFile(zip_buffer, 'r') as zip_ref:
            zip_ref.extractall('./'+ institution +'_fake')
            name = zip_ref.namelist()[0].split('/')[0]
        zip_buffer.close()

        txt_datei = './'+ institution +'_fake/' + name + '/0.last_redirect.txt'

        # Pfad zur CSV-Datei
        csv_datei = './'+ institution +'_fake/'+ institution +'_urls.csv'

        # Datei lesen und in CSV schreiben
        with open(txt_datei, 'r') as txt_file, open(csv_datei, 'a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([uuid])

            for zeile in txt_file:
                # Zeile in eine Liste von Werten aufteilen
                daten = zeile.strip().split(',')
                # Daten in die CSV-Datei schreiben
                csv_writer.writerow(daten)

        csv_datei = './'+ institution +'_fake/'+ institution +'_takedown_info.csv'

        # Datei lesen und in CSV schreiben
        with open(csv_datei, 'a') as f_object:
            writer_object = writer(f_object)
            writer_object.writerow([uuid])
            writer_object.writerow(lookyloo.get_takedown_information(uuid))
            f_object.close()

