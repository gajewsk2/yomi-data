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

def inReading(character, expression, data):
    for r in data[character]['reading']:
        if r in expression:
            print(expression)
            print(data[character]['raw'])
            return True
    return False


def injectReadingData(data, cards_file, output):
    remove_file(output)
    with open(output, "a") as myfile:
        n=0
        for i in open(cards_file, encoding="utf8").readlines():
            # expression = [splits for splits in i.split("\t") if splits is not ""][5]

            phonetics = []
            expression = i.split("\t")[0]

            for c in expression:
                if c in data:
                    if inReading(c, expression,data):
                        if data[c]['raw'] not in phonetics:
                            phonetics.append(data[c]['raw'])
            if phonetics:
                n = n+ 1

            row = i.split("\t")
            row[28] = '<br>'.join(phonetics)
            myfile.write('\t'.join(row))
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
