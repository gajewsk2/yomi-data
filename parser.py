import os
import re
import json


def remove_file(filename):
    try:
        os.remove(filename)
    except FileNotFoundError:
        pass


def getChars(i):
    char_delim = '→'
    chars = i[i.index(char_delim) + 1:]
    chars = list(re.sub('[, \n]', '', chars))
    return chars


def getRadical(i):
    r = i[0]
    return r


def getReading(i):
    reading = re.search('\((.*?)\)', i).group(1)
    reading = reading.split(', ')
    # print(reading)
    return reading

def inReading(idx, character, expression, data):
    # print(expression[idx:])
    expression = expression[idx:]
    expression = expression[:expression.index(']')]
    for r in data[character]['reading']:
        if r in expression:
            # print(expression)
            # print(data[character]['raw'])
            return True
    return False


def injectReadingData(data, cards_file, output):
    remove_file(output)
    with open(output, "a", encoding="utf8") as myfile:
        n=0
        for i in open(cards_file, encoding="utf8").readlines():
            # expression = [splits for splits in i.split("\t") if splits is not ""][5]

            phonetics = []
            expression = i.split("\t")[0]

            for idx, c in enumerate(expression):
                if c in data:
                    if inReading(idx, c, expression,data):
                        if data[c]['raw'] not in phonetics:
                            raw = data[c]['raw']
                            delim_index = raw.index('→')
                            chars = (raw)[delim_index:]
                            highlight_index = (chars).index(c)
                            total_index = delim_index + highlight_index
                            highlighted = raw[:total_index]+'<b>'+ c +'</b>'+raw[total_index+1:]
                            phonetics.append(highlighted)
            if phonetics:
                n = n+ 1

            row = i.split("\t")
            row[28] = '<br>'.join(phonetics)
            myfile.write('\t'.join(row))
            # print('\t'.join(row))
            # print(expression)
        print(n)


def main():
    input_file = 'yomi.txt'
    cards_file = 'core.txt'
    json_output = 'data.json'
    cards_output = 'test.txt'
    data = getReadingData(input_file)
    injectReadingData(data, cards_file, cards_output)
    # dumper(data, json_output)


def getReadingData(input_file):
    data = {}
    for i in open(input_file, encoding="utf8").readlines():
        chars = getChars(i)
        radical = getRadical(i)
        reading = getReading(i)
        for c in chars:
            data[c] = {}
            data[c]['raw'] = i.replace('\n', '')
            data[c]['radical'] = radical
            data[c]['reading'] = reading
            data[c]['relative'] = chars
    return data


def dumper(data, output):
    # print(data)
    remove_file(output)
    with open(output, 'w') as outfile:
        json.dump(data, outfile, ensure_ascii=False)


if __name__ == '__main__':
    main()
