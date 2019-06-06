'''
    Cr
'''

import os, re, sys, time, unicodedata, math, csv, collections
import sqlite3

dbName = "ecrains.db"

def executeArgs():
    index = 1
    while index < len(sys.argv):

        if sys.argv[index] == '-ad':
            index += 1
            if os.path.exists(sys.argv[index]):
                newData = lireFile(sys.argv[index])
                addData(newData)

        index += 1

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
    # file = getFileArg()
    fileObj = open(file)
    content = fileObj.read()
    dataList = list()
    headers = None
    deli = input("please enter the type of delimiter being used:\n>")
    name = input("Please enter the name where this data comes from:\n>")
    with open(file, 'r') as fileContent:
        fileContent = csv.reader(fileContent, delimiter=deli)
        headers = next(fileContent)
        data = collections.namedtuple(name, headers)
        for row in fileContent: dataList.append(data(*row))
    # print(dataList)
    # openDatabase(dataList)
    return (dataList, name, headers)

def addData(dataPack):
    '''
    '''
    global dbName
    dataList, name, headers = dataPack
    try:
        dbObj = sqlite3.connect(dbName)
        cursorObj = dbObj.cursor()
        cursorObj.execute('SELECT name from sqlite_master where type= "table"')
        tables = cursorObj.fetchall()
        for tup in tables:
            if name in tup:
                print("WARNING: table found, overwrite existing data?")
                confirmation = input("y/n?\n>")
                if not confirmation == 'y': return
                cursorObj.execute("DROP TABLE IF EXISTS {}; ".format(name))
        tableTypes = '{} char(150), ' * (len(headers)-1)
        tableTypes = tableTypes[:-2].format(*headers)
        newTable = 'create table {} ( UID integer primary key, {});'.format(name,tableTypes)
        cursorObj.execute(newTable)
        values = '?,' * len(headers)
        statement = 'insert into {} values ({})'.format(name, values[:-1])
        print(statement)
        cursorObj.executemany(statement, dataList)
    except:
        print(sys.exc_info()[0])
        input("> ")
    finally:
        dbObj.commit()
        cursorObj.close()
        dbObj.close()
    return


def mainmenu():
    '''
    '''
    print("What do you want to do? Options:")
    print("(vat) view all tables, (ss) sql select, (h) help, (q) quit")
    choice = ''
    while choice != 'q':
        choice = input("What do you want to do?\n> ")
        if choice == 'vat':
            viewTables()
        elif choice == 'ss':
            selectStatement()
    return

def selectStatement():
    '''
    '''
    global dbName

    print("There are 3 parts: SELECT, FROM, WHERE")
    sel = input("input the SELECT part\n>")
    frm = input("input the FROM part\n>")
    whr = input("input the WHERE part\n>")

    try:
        dbObj = sqlite3.connect(dbName)
        cursorObj = dbObj.cursor()
        if whr == '':
            # statement = 'SELECT ? FROM ? '
            # cursorObj.execute(statement, [sel, frm])
            # cursorObj.execute('select ? from refuge', (sel))
            cursorObj.execute("select {} from {}".format(sel, frm))
        else:
            statement = 'SELECT ? FROM ? WHERE ?;'
            cursorObj.execute(statement, [sel, frm, whr])
        tables = cursorObj.fetchall()
        print("Results:\n{}".format(tables))
    finally:
        cursorObj.close()
        dbObj.close()
    return

def viewTables():
    '''
    '''
    global dbName
    try:
        dbObj = sqlite3.connect(dbName)
        cursorObj = dbObj.cursor()
        cursorObj.execute('SELECT name from sqlite_master where type= "table"')
        tables = cursorObj.fetchall()
        print("current tables:\n{}".format(tables))
    finally:
        cursorObj.close()
        dbObj.close()

    return

def main():
    executeArgs()
    mainmenu()

    return

if __name__ == '__main__':
    main()
