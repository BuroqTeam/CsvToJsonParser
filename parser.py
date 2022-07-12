import csv
import json
import argparse
import datetime


def make_json(csvFilePath, jsonFilePath):
    # Create JSON Schema
    data = {
        'meta': {
            'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'inputCsv': csvFilePath,
            'outputJson': jsonFilePath
        },
        'questions': []
    }

    # Open CSV File and read it
    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)

        for row in csvReader:
            # Skip if questions is empty
            if row['question']:
                question = {
                    'id': row['id'],
                    'meta': {
                        'subject': row['subject'],
                        'class': row['class'],
                        'chapter': row['chapter'],
                        'number': row['number'],
                        'pattern': row['pattern'],
                    },
                    'question': {
                        'title': row['question'],
                        'options': []
                    }
                }

                # Iterate through all options of the question
                for key, value in row.items():
                    if key.startswith('option'):
                        question['question']['options'].append(value)

                # Add the question to the list
                data['questions'].append(question)

    # Open a json writer, and use the json.dumps() to dump data
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(data, indent=4))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--csv", help="(Required) Path of input CSV file to create a JSON file from", required=True)
    parser.add_argument(
        "--outJson", help="(Optional) Path of output JSON file that is generated from CSV File.")
    args = parser.parse_args()

    csvFilePath = args.csv
    jsonFilePath = f"{csvFilePath}-out.json"

    if args.outJson:
        jsonFilePath = args.outJson

    make_json(csvFilePath, jsonFilePath)
