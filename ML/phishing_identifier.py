import csv
import pandas as pd

companies = ["amazon", "ameli", "amendes", "atandt", "credit_agricole", "luxtrust", "microsoft", "netflix", "orange", "paypal"]

for company in companies:
    print(company)
    #getting the results
    data_path = company + "_results_rf.csv"
    data = pd.read_csv(data_path)
    filtered_data = data[data['prediction'] == 1]

    ips = pd.read_csv("ips_list/" + company + '_ips.csv')
    #getting dataset
    data_path = "datasets/" + company + "_dataset.csv"
    data_all = pd.read_csv(data_path)

    for index, row in filtered_data.iterrows():
        uuid = row['uuid']
        filtered_data_all = data_all[data_all['uuid'] == uuid]
        ip = filtered_data_all['ip'].iloc[0]
        third_party_hits = filtered_data_all['3rd_party_hits'].iloc[0]
        #ip_found = ips[ips.apply(lambda row: ip in row.values, axis=1)]
        ip_found = ips[ips['ip'] == ip]

        malicious = filtered_data_all['malicious'].iloc[0]
        if not ip_found.empty:
            print(f'uuid: {uuid} is not malicious. What it is marked in the dataset :{malicious}')
        elif third_party_hits > 0:
            print(f'uuid: {uuid} is surely malicious. What it is marked in the dataset :{malicious}')
        else:
            print(f'uuid: {uuid} might be malicious. What it is marked in the dataset :{malicious}')
