
import csv
import ast

# Pfad zur CSV-Datei
takedown_path = "/home/amaraj/Bachelorarbeit/capture_saver/amazon_fake/amazon_takedown_info.csv"

# Datei einlesen
with open(takedown_path, mode='r', encoding='utf-8') as file:
    reader = csv.reader(file)
    rows = list(reader)

    # Durch die Zeilen in 2er-Schritten iterieren
    for i in range(0, len(rows), 2):
        uuid_row = rows[i]
        info_row = rows[i + 1] if i + 1 < len(rows) else None

        # Überprüfen, ob die UUID-Zeile und die Information-Zeile existieren
        if uuid_row and len(uuid_row) > 0 and uuid_row[0] == "5309d833-0c27-46a5-8351-b9acc7f7795c":
            if info_row and len(info_row) > 0:
                try:
                    # Die Elemente der Info-Zeile als Strings behandeln
                    dict_strings = info_row

                    # Jeden String in ein Python-Dictionary umwandeln
                    dict_list = [ast.literal_eval(d) for d in dict_strings]

                    # Resultat anzeigen
                    print(dict_list)

                except (ValueError, SyntaxError) as e:
                    print("Error:", e)



# Deine CSV-Zeile


# Die CSV-Zeile in eine Liste von Strings aufteilen
