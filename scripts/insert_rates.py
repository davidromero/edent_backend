import csv
import json
import boto3

TABLE_NAME = 'treatment_rates_chiquimula'
FILE_PATH = './input/Tarifario.csv'

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

table = dynamodb.Table(TABLE_NAME)

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
                body[key] = row[item_count]
                item_count += 1
            line_count += 1
            print('Inserting: ' + json.dumps(body))
            table.put_item(
                Item=body
            )
    print(f'Processed {line_count} lines.')
