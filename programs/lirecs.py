'''
    Cr
'''

import os, re, sys, time, unicodedata, math, csv


def getFileArg():
    if len(sys.argv) < 2:
        print("ERROR: not enough argv")
        sys.exit()
    file = sys.argv[1]
    if not os.path.exists(file):
        print("ERROR: file doesn't exist")
        sys.exit()
    return file

def lireFile(file):
    fileObj = open(file)
    content = fileObj.read()
    with open(file, 'r') as fileContent:
        fileContent = csv.reader(fileContent, delimiter='\t')

        for row in fileContent:
            print(row)
            input("> ")


def main():

    file = getFileArg()

    lireFile(file)

    return

if __name__ == '__main__':
    main()
