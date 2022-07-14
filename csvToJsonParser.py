import csv
import json
import argparse
import datetime
import pathlib


def print_error_message(questionId: str, param: str, paramValue: str, requiredParamValue: str):
    print(
        f"ERROR: {questionId} {param} '{paramValue}' does not match the required {param} '{requiredParamValue}'")
    print("Aborting JSON generation")


def valid_question(grade: str, subject: str, language: str, question: map) -> bool:
    if question['grade'] != grade:
        print_error_message(question['id'], 'grade', question['grade'], grade)
        return False

    if question['subject'] != subject:
        print_error_message(question['id'], 'subject',
                            question['subject'], subject)
        return False

    if question['language'] != language:
        print_error_message(
            question['id'], 'language', question['language'], language)
        return False

    return True


def make_json(csvPath, jsonFilePath, grade, subject, language):
    # Create JSON Schema
    data = {
        'meta': {
            'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'grade': grade,
            'subject': subject,
            'language': language
        },
        'chapters': []
    }

    chapters = {}

    for csvFile in pathlib.Path(csvPath).glob('*.csv'):
        # Open CSV File and read it
        with open(csvFile, encoding='utf-8') as csvf:
            csvReader = csv.DictReader(csvf)

            for row in csvReader:
                if row['question']:
                    # Make sure each question metadata matches the User Input
                    if not valid_question(grade, subject, language, row):
                        exit(1)

                    if row['chapter'] not in chapters:
                        chapters[row['chapter']] = {
                            'number': row['chapter'],
                            'name': row['chapterName'],
                            'questions': []
                        }

                    question = {
                        'id': row['id'],
                        'pattern': row['pattern'],
                        'question': {
                            'title': row['question']
                        }
                    }

                    match int(row['pattern']):
                        case 1:
                            question['question']['options'] = row['options'].split(
                                ',')
                        case 2:
                            question['question']['options'] = row['options'].split(
                                ',')
                        case other:
                            print(
                                f"Parser not implemented for pattern {row['pattern']}")
                            continue

                    # Remove double-quotes from options
                    for i in range(len(question['question']['options'])):
                        option = question['question']['options'][i]

                        if option[0] == '"' and option[-1] == '"':
                            question['question']['options'][i] = option[1:-1]

                    chapters[row['chapter']]['questions'].append(question)

    for _, value in chapters.items():
        data['chapters'].append(value)

    data['chapters'] = sorted(data['chapters'], key=lambda x: x['number'])

    # Open a json writer, and use the json.dumps() to dump data
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(data, indent=4))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--csv", help="(Required) Path of folder where CSV files to create a JSON file from are located.", required=True)
    parser.add_argument(
        "--grade", help="(Required) Grade Number that the questions belong to.", required=True)
    parser.add_argument(
        "--subject", help="(Required) Subject that the questions belong to.", required=True)
    parser.add_argument(
        "--language", help="(Required) Language Code (Uz, Kaz, Kar, Kir, Ru) of the questions.", required=True)
    parser.add_argument(
        "--outJson", help="(Optional) Path of output JSON file that is generated from CSV Files.")
    args = parser.parse_args()

    csvPath = args.csv
    jsonFilePath = f"{csvPath}/questions-out.json"

    if args.outJson:
        jsonFilePath = args.outJson

    make_json(csvPath, jsonFilePath, args.grade,
              args.subject.lower(), args.language.lower())
