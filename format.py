import json

# Open the JSON file with UTF-8 encoding
with open('last.json', encoding='utf-8') as f:
    # Load the JSON data
    data = json.load(f)

# print(json.dumps(data, indent=4))

"""
{
    "ranks": [
        {
            "stats_rank": "15",
            "stats_label": "МЯСТО В ПАРАЛЕЛКАТА"
        },
        {
            "stats_rank": "102",
            "stats_label": "МЯСТО ВЪВ ВИПУСКА"
        }
    ],
    "statistics": [
        {
            "desc": "Успех",
            "number": "5.65",
            "link": "https://app.shkolo.bg/diary/pupil/2300566279#tab_grades"
        },
    ]
}
"""

statistics={}
for rank in data['ranks']:
    statistics[rank['stats_label']] = rank['stats_rank']

for stat in data['statistics']:
    statistics[stat['desc']] = stat['number']


"""
   "grades": [
        {
            "course": "Български език и литература",
            "term1Final": "5",
            "term1Current": [
                "4",
                "6",
                "5",
                "5"
            ],
            "term2Final": "",
            "term2Current": [],
            "final": ""
        }
    ]
"""
# iterate over the data grades

grades = {}
for grade in data['grades']:
    # Add the grade to the result
    grades[grade['course']] = {
        'Първи срок': {
            "Срочна оценка" : grade['term1Final'],
            "Текуща оценка" : grade['term1Current']
        },
        'Втори срок': { 
            "Срочна оценка" : grade['term2Final'],
            "Текуща оценка" : grade['term2Current']
        },
        'Годишна': grade['final']
    }


result = {}
result['Статистика'] = statistics
result['Оценки'] = grades


with open('last-f.json', 'w', encoding='utf-8') as file:
    json.dump(result, file, indent=4, ensure_ascii=False)

print('Done!')