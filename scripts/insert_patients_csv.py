import csv
import json
import requests

TABLE_NAME = ''
FILE_PATH = './input/Listado pacientes.csv'

with open(FILE_PATH, 'r', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    headers = None
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            headers = row
            line_count += 1
        else:
            body = {}
            item_count = 0
            for key in headers:
                if item_count > 0:
                    if key == 'doctor_names':
                        body[key] = []
                    else:
                        body[key] = row[item_count]
                item_count += 1
            line_count += 1

            res = requests.post('https://rwcmecc1l5.execute-api.us-east-1.amazonaws.com/api/patients/',
                                data=json.dumps(body),
                                headers={'Content-type': 'application/json', 'Accept': 'application/json'})
            if res.status_code is 201:
                print(f'Inserted: {row[0]}')
            else:
                print(f'Failed: {row[0]} {res.text}')
    print(f'Processed {line_count} lines.')
