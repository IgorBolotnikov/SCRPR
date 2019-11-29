import json

with open('jobs_list__work_ua.json') as file:
    for line in json.load(file):
        for key, value in line.items():
            print(f'{key}: {value}')
        print()
