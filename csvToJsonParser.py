import csv
import json
import argparse
import datetime
import pathlib


def print_error_message(questionId: str, param: str, paramValue: str, requiredParamValue: str):
    print(f"ERROR: {questionId} {param} '{paramValue}' does not match the required {param} '{requiredParamValue}'")
    print("Aborting JSON generation")


def validate_question(question: map):
    params = ['options', 'problem', 'solution', 'statements']

    for param in params:
        if param in question['question'] and len(question['question'][param]) == 0:
            print(f"WARNING: {question['id']} has empty params: {param}.")


def valid_question(grade: str, subject: str, language: str, question: map) -> bool:
    if question['grade'] != grade:
        print_error_message(question['id'], 'grade', question['grade'], grade)
        return False

    if question['subject'] != subject:
        print_error_message(question['id'], 'subject', question['subject'], subject)
        return False

    if question['language'] != language:
        print_error_message(question['id'], 'language', question['language'], language)
        return False

    return True


def parse_options(questionId: str, rawOptions: str) -> list:
    res = []
    newLine = '\n'
    rawOptions = rawOptions.rstrip().lstrip()

    if newLine in rawOptions:
        # print(f"\nWARNING: parse_options(): {questionId} contains a New Line in it:\n==========")
        # print(f"{rawOptions}\n==========")
        # print("CHECK IF THE NEW LINE IS INTENTIONAL")
        rawOptions = f'"{rawOptions}"'

    try:
        for line in csv.reader([rawOptions.strip()], skipinitialspace=True):
            for item in line:
                res.append(item.strip())
    except Exception as ex:
        print(f"parse_options(): Error in parsing {questionId}: {ex}")
        print(rawOptions)

    return res


def parse_complex_options(questionId: str, rawOptions: str) -> list:
    res=[]
    rawOptions = rawOptions.split('[sss]')

    try:
        for split in rawOptions:
            split = split.strip().removeprefix('[').removesuffix(']')
            options = []

            for line in csv.reader([split], skipinitialspace=True):
                for item in line:
                    options.append(item.strip())
            
            res.append(options)
    except Exception as ex:
        print(f"parse_complex_options(): Error in parsing {questionId}: {ex}")    
    
    return res


def parse_options_for_26(questionId: str, rawOptions: str) -> list:
    res = []
    rawOptions = rawOptions.split('[sss]')

    try:
        for split in rawOptions:
            split = split.strip().removeprefix('[').removesuffix(']')
            options = []

            for line in csv.reader([split], skipinitialspace=True):
                for item in line:
                    options.append(item.strip())

            split = ",".join(options[1:-1])
            split = split.strip().removeprefix('[').removesuffix(']')

            cleanOptions = [options[0]]

            for line in csv.reader([split], skipinitialspace=True):
                for item in line:
                    cleanOptions.append(item.strip())

            cleanOptions.append(options[-1])
            res.append(cleanOptions)
    except Exception as ex:
        print(f"parse_complex_options(): Error in parsing {questionId}: {ex}")

    return res


def make_json(csvPath, jsonFilePath, grade, subject, language):
    # Create JSON Schema
    data = {
        'meta': {
            'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'grade': int(grade),
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
                if 'question' in row and row['question']:
                    # Make sure each question metadata matches the User Input
                    if not valid_question(grade, subject, language, row):
                        exit(1)

                    if row['chapter'] not in chapters:
                        chapters[row['chapter']] = {
                            'number': int(row['chapter']),
                            'name': row['chapterName'],
                            'description': row['description'],
                            'questions': []
                        }

                    question = {
                        'id': row['id'],
                        'pattern': int(row['pattern']),
                        'question': {
                            'title': row['question']
                        }
                    }

                    # Patterns 1,2,7,11,12,13,18,17,19,20,21,23,25,27
                    if row['pattern'] == "1" or row['pattern'] == "2" or row['pattern'] == "7" or row['pattern'] == "11" or \
                        row['pattern'] == "12" or row['pattern'] == "13" or row['pattern'] == "17" or row['pattern'] == "18" or \
                        row['pattern'] == "19" or row['pattern'] == "20" or row['pattern'] == "21" or row['pattern'] == "23" or row['pattern'] == '25' or \
                        row['pattern'] == '27':
                        # Parse Options
                        question['question']['options'] = parse_options(row['id'], row['options'])
                    elif row['pattern'] == "3" or row['pattern'] == "5":
                        # Parse Problem
                        question['question']['problem'] = parse_options(row['id'], row['problem'])
                        # Parse Solution
                        question['question']['solution'] = parse_complex_options(row['id'], row['solution'])
                    elif row['pattern'] == "4":
                        question['question']['statements'] = []
                        question['question']['options'] = []
                        rawStatements = row['statement'].split('[sss]')
                        rawOptions = row['options'].split('[sss]')
                        
                        # Parse Statement
                        for statement in rawStatements:
                            statement = statement.strip().removeprefix('[').removesuffix(']')
                            
                            for line in csv.reader([statement], skipinitialspace=True):
                                question['question']['statements'].append({
                                    'statement': line[0],
                                    'image': line[1]
                                })
                        
                        # Parse Options
                        for option in rawOptions:
                            option = option.strip().removeprefix('[').removesuffix(']')
                            
                            for line in csv.reader([option], skipinitialspace=True):
                                question['question']['options'].append({
                                    'left': line[0],
                                    'sign': line[1],
                                    'right': line[2]
                                })
                    # Patterns 6,14,15,16,22,24
                    elif row['pattern'] == "6" or row['pattern'] == "14" or row['pattern'] == "15" or row['pattern'] == '16' or row['pattern'] == '22' or row['pattern'] == '24':                     
                        question['question']['problem'] = parse_options(row['id'], row['problem'])
                        question['question']['solution'] = parse_options(row['id'], row['solution'])
                    elif row['pattern'] == "8":
                        question['question']['figureType'] = row['figureType']
                        question['question']['proportion'] = parse_options(row['id'], row['proportion'])
                    elif row['pattern'] == "9":
                        question['question']['options'] = []
                        rawOptions = row['options'].split('[sss]')
                        
                        for option in rawOptions:
                            option = option.strip().removeprefix('[').removesuffix(']')

                            for line in csv.reader([option], skipinitialspace=True):
                                question['question']['options'].append({
                                    'left': line[0],
                                    'sign': line[1],
                                    'right': line[2]
                                })
                    elif row['pattern'] == "10":
                        question['question']['statements'] = parse_complex_options(row['id'], row['statement'])
                        question['question']['options'] = parse_complex_options(row['id'], row['options'])                    
                    elif row['pattern'] == "26":                        
                        question['question']['options'] = parse_options_for_26(row['id'], row['options'])                        
                    else:
                        print(f"Parser not implemented for pattern {row['pattern']}")
                        continue

                    validate_question(question)
                    chapters[row['chapter']]['questions'].append(question)

    for _, chapter in chapters.items():
        chapter['questions'] = sorted(chapter['questions'], key=lambda x: x['pattern'])
        data['chapters'].append(chapter)

    data['chapters'] = sorted(data['chapters'], key=lambda x: x['number'])

    # Open a json writer, and use the json.dumps() to dump data
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(data, indent=4))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", help="(Required) Path of folder where CSV files to create a JSON file from are located.", required=True)
    parser.add_argument("--grade", help="(Required) Grade Number that the questions belong to.", required=True)
    parser.add_argument("--subject", help="(Required) Subject that the questions belong to.", required=True)
    parser.add_argument("--language", help="(Required) Language Code (Uz, Kaz, Kar, Kir, Ru) of the questions.", required=True)
    parser.add_argument("--outJson", help="(Optional) Path of output JSON file that is generated from CSV Files.")
    args = parser.parse_args()

    csvPath = args.csv
    jsonFilePath = f"{csvPath}/questions-out.json"

    if args.outJson:
        jsonFilePath = args.outJson

    make_json(csvPath, jsonFilePath, args.grade,args.subject.lower(), args.language.lower())
