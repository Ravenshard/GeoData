'''
    Cr
'''

import os, re, sys, time, unicodedata, math, csv, collections


def getFileArg():
    '''
    '''
    if len(sys.argv) < 2:
        print("ERROR: not enough argv")
        sys.exit()
    file = sys.argv[1]
    if not os.path.exists(file):
        print("ERROR: file doesn't exist")
        sys.exit()
    return file

def lireFile(file):
    '''
    '''
    fileObj = open(file)
    content = fileObj.read()
    dataList = list()
    deli = input("please enter the type of delimiter being used:\n>")
    name = input("Please enter the name where this data comes from:\n>")
    with open(file, 'r') as fileContent:
        fileContent = csv.reader(fileContent, delimiter=deli)
        ecrainsData = collections.namedtuple(name, next(fileContent))
        for row in fileContent: dataList.append(ecrainsData(*row))
    print(dataList)

def main():

    file = getFileArg()

    lireFile(file)

    return

if __name__ == '__main__':
    main()
