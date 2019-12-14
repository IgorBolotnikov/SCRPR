import json

with open('jobs_list__work_ua.json') as file:
    print(len(json.load(file)))
    # for line in json.load(file):
    #     for key, value in line.items():
    #         print(f'{key}: {value}')
