'''
    Cr
'''

import os, re, sys, time, unicodedata, math, csv, collections
import sqlite3

dbName = "ecrains.db"

def executeArgs():
    ''' Execute all arguments from the command line before running the program
    parameters:
        None

    Returns:
        None
    '''
    index = 1
    while index < len(sys.argv):

        if sys.argv[index] == '-ad':
            index += 1
            if os.path.exists(sys.argv[index]):
                newData = lireFile(sys.argv[index])
                addData(newData)

        index += 1
    return

def lireFile(file):
    ''' Lire le file avec la donnée adjouter le base de donnée
    Parameters:
        Aucun

    Returns:
        Aucun
    '''
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
    return (dataList, name, headers)

def addData(dataPack):
    ''' Add data to the existing db
    Parameters:
        dataPack (tuple):   All the data extracted from a file to add to the db

    Returns:
        None
    '''
    global dbName
    dataList, name, headers = dataPack
    try:
        dbObj = sqlite3.connect(dbName)
        cursorObj = dbObj.cursor()
        cursorObj.execute('SELECT name from sqlite_master where type= "table"')
        tables = cursorObj.fetchall()
        # Handle overwriting tables
        if tables != []:
            for tup in tables:
                if name in tup:
                    print("WARNING: table found, overwrite existing data?")
                    confirmation = input("y/n?\n>")
                    if not confirmation == 'y': return
                    cursorObj.execute("DROP TABLE IF EXISTS {}; ".format(name))
        tableTypes = '{} char(150), ' * (len(headers))
        tableTypes = tableTypes[:-2].format(*headers)
        newTable = 'create table {} ({});'.format(name, tableTypes)
        cursorObj.execute(newTable)
        values = '?,' * len(headers)
        statement = 'insert into {} values ({})'.format(name, values[:-1])
        cursorObj.executemany(statement, dataList)
    except Exception as inst:
        print(type(inst))
        print(inst)
        input("> ")
    finally:
        dbObj.commit()
        cursorObj.close()
        dbObj.close()
    return

def mainmenu():
    ''' Print the main menu of options available to the user
    Parameters:
        None

    Returns:
        None
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
        # elif choice == 'th':
        #     tableHeaders()
    return

def selectStatement():
    ''' User inputs a select statement from cmd line that the program executes
    Parameters:
        None

    Returns:
        None
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
            # statement = 'SELECT ? FROM ? WHERE ?;'
            cursorObj.execute("select {} from {} where {}".format(sel, frm, whr))
            # cursorObj.execute(statement, [sel, frm, whr])
        tables = cursorObj.fetchall()
        print("Results:\n{}".format(tables))
    except Exception as inst:
        print(type(inst))
        print(inst)
        input("> ")
    finally:
        cursorObj.close()
        dbObj.close()
    return

def viewTables():
    ''' View all the tables in the current database
    Parameters:
        None

    Returns:
        None
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
