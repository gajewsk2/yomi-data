import os
import re
import json

def remove_file(filename):
    try:
        os.remove(filename)
    except FileNotFoundError:
        pass


# def getReading(kanji):
#     if
#         readings = [strip_tags(i).replace('[sound:', '\t[sound:') for i in open(input_file, encoding="utf8").readlines()]
#     return

def getChars(i):
    char_delim = '→'
    chars = i[i.index(char_delim) + 1:]
    chars = list(re.sub('[, \n]', '', chars))
    return chars

def getRadical(i):
    r = i[0]
    return r

def getReading(i):
    reading = re.search('\((.*?)\)',i).group(1)
    reading = reading.split(', ')
    print(reading)
    return reading

def main():
    input_file = 'yomi.txt'
    full_data = 'core.txt'
    output = 'output/1.csv'
    remove_file(output)
    data = {}
    i = open(input_file, 'r')
    for i in open(input_file, encoding="utf8").readlines():
        # chars = chars.split(',')
        # chars = chars.split(',')
        chars = getChars(i)
        radical = getRadical(i)
        reading = getReading(i)
        for c in chars:
            data[c] = {}
            data[c]['raw'] = i.replace('\n', '')
            data[c]['radical'] = radical
            data[c]['reading'] = reading
            data[c]['relative'] = chars
        # data['chars'] =

    # print(data)


    with open('data.json', 'w') as outfile:
        json.dump(data, outfile, ensure_ascii=False)


        # clean_i = strip_tags(li)

        # o = open(output, 'a+', encoding="utf8")
        # for item in list_i:
        #     o.write("%s\n" % item)
        # # o.write(li.encode('utf8'))
        # o.close()
        #


if __name__ == '__main__':
    main()
