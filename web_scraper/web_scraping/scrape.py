

def clean_keywords(input):
    alphabet = '''абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТ
УФХЦЧШЩЪЫЬЭЮЯabcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ '''
    res = ''
    for char in input:
        if char in alphabet:
            res += char
    return res


def filter_keywords(input):
    output = []
    for word in input:
        if len(word) > 2:
            output.append(word)
    return output


def sort_by_relevance(array, field, crosscheck, keywords, output=[]):
    output = []
    result = []
    filtered = []
    for keyword in keywords:
        for item in array:
            if keyword.lower() in item[field].lower():
                result.append(item)
        output += result
        array = result.copy()
        result.clear()
    output.reverse()
    values = []
    crosslist = []
    for item in output:
        if item[field] not in values or item[crosscheck] not in crosslist:
            filtered.append(item)
            values.append(item[field])
            crosslist.append(item[crosscheck])
    return filtered
