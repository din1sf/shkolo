import json

# Open the JSON file with UTF-8 encoding
with open('2024-03-03.json', encoding='utf-8') as f:
    # Load the JSON data
    data = json.load(f)

'''
"subjects": [
        {
            "subject": "Български език и литература",
            "term1": {
                "final": "5",
                "current": [
                    "4",
                    "6",
                    "5",
                    "5"
                ]
            },
            "term2": {
                "final": "",
                "current": []
            },
            "year": ""
        },
'''

selected_term = 'term2'

term_subjects = {}
for subject in data['subjects']:
    term_subjects[subject['subject']] = subject[selected_term]['current']
    
result = {}
result['statistics'] = data['statistics']
result['subjects'] = term_subjects

print(result)

with open('grades.json', 'w', encoding='utf-8') as file:
    json.dump(result, file, indent=4, ensure_ascii=False)

print('Done!')