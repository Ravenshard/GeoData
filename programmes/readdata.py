'''
    HOW TO ADD IMAGES TO DATABASE:
    run program as follows:
        python .\programmes\readdata.py -apf .\photos
    It will take some time, but it should say 'Photos added successfully'
    after some time.  After you can hit 'q' to quit, and all is good.

'''

import os, re, sys, time, unicodedata, math, csv, collections, locale
import psycopg2
from PIL import Image

user = "Jay"

def getConnection():
    ''' Connect to the database and return connection and cursor
    Parameters:
        None

    Returns:
        connection:     connection to the database
        cursor:         cursor to be used with the database
    '''
    global user
    connect_str = "dbname='ecrains' user='{}' host='localhost' ".format(user) + \
                  "password='inriaTravail19'"
    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()
    return (conn, cursor)

def getSecureConnection():
    ''' Connect to the database and return connection and cursor
    Parameters:
        None

    Returns:
        connection:     connection to the database
        cursor:         cursor to be used with the database
    '''
    global user
    pw = input("please enter password:\n> ")
    connect_str = "dbname='ecrains' user='{}' host='localhost' ".format(user) + \
                  "password='{}'".format(pw)
    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()
    return (conn, cursor)

def closeConnection(conn, cursor):
    ''' Close the connection with the database
    Parameters:
        conn:       connection to be closed
        cursor:     cursor to be closed

    Returns:
        None
    '''
    cursor.close()
    conn.close()
    return

def executeArgs():
    ''' Execute all arguments from the command line before running the program
    parameters:
        None

    Returns:
        None
    '''
    index = 1
    while index < len(sys.argv):
        if sys.argv[index] == '-test':
            testStatement()
        elif sys.argv[index] == '-ad':
            index += 1
            if os.path.exists(sys.argv[index]):
                newData = lireFile(sys.argv[index])
                addData(newData)
        elif sys.argv[index] == '-del':
            index += 1
            deleteTable(sys.argv[index])
        elif sys.argv[index] == '-apf':
            index +=1
            if os.path.exists(sys.argv[index]):  addPhotoFile(sys.argv[index])
        index += 1
    return

def lireFile(file):
    ''' Lire le file avec la donnée adjouter le base de donnée
    Parameters:
        file (str):     le chemin où les données sont stockées

    Returns:
        Aucun
    '''
    fileObj = open(file)
    content = fileObj.read()
    dataList = list()
    headers = None
    deli = input("please enter the type of delimiter being used:\n>")
    name = input("Please enter the name where this data comes from:\n>")
    with open(file, "r") as fileContent:
        fileContent = csv.reader(fileContent, delimiter=deli)
        headers = next(fileContent)
        data = collections.namedtuple(name, headers)
        for row in fileContent:  dataList.append(data(*row))
    return (dataList, name, headers)

def addPhotoFile(file):
    ''' TODO: Take apart and make smaller
    '''
    try:
        allPhotos = os.listdir(file)
        dbObj, cursorObj = getSecureConnection()

        cursorObj.execute('SELECT tablename FROM pg_catalog.pg_tables;')
        tables = cursorObj.fetchall()
        # Handle overwriting tables
        bool = True
        for tup in tables:
            if 'photos' in tup:
                bool = False
        if bool:
            statement = "CREATE TABLE Photos (uid text, picid text, ext text, photo bytea, primary key (uid, picid) );"
            cursorObj.execute(statement)

        for photo in allPhotos:
            (uid, picid, ext) = photo.split('.')
            binPhoto = open("{}.\\{}".format(file,photo), 'rb').read()
            statement = "INSERT INTO Photos(uid, picid, ext, photo) VALUES (%s, %s, %s, %s)"
            cursorObj.execute(statement, (uid, picid, ext, psycopg2.Binary(binPhoto)))
    except Exception as inst:
        print(type(inst))
        print(inst)
        input("> ")
    finally:
        dbObj.commit()
        closeConnection(dbObj, cursorObj)
        print("Photos added successfully")
    return

def addData(dataPack):
    ''' Add data to the existing db
    Parameters:
        dataPack (tuple):   All the data extracted from a file to add to the db

    Returns:
        None
    '''
    dataList, name, headers = dataPack
    try:
        dbObj, cursorObj = getSecureConnection()
        cursorObj.execute('SELECT tablename FROM pg_catalog.pg_tables;')
        tables = cursorObj.fetchall()
        # Handle overwriting tables
        for tup in tables:
            if name in tup:
                print("WARNING: table found, overwrite existing data?")
                confirmation = input("y/n?\n>")
                if not confirmation == 'y': return
                cursorObj.execute("DROP TABLE IF EXISTS {}; ".format(name))
        tableTypes = '{} text, ' * (len(headers))
        tableTypes = tableTypes[:-2].format(*headers)
        newTable = 'create table {} ({});'.format(name, tableTypes)
        cursorObj.execute(newTable)
        values = '%s,' * len(headers)
        statement = 'insert into {} values ({})'.format(name, values[:-1])
        cursorObj.executemany(statement, dataList)
    except Exception as inst:
        print(type(inst))
        print(inst)
        input("> ")
    finally:
        dbObj.commit()
        closeConnection(dbObj, cursorObj)
        print("Table added successfully")
    return

def deleteTable(tableName):
    ''' Delete a table from the database
    Parameters:
        tableName (str):    the name of the table we will delete

    Returns:
        None
    '''
    try:
        dbObj, cursorObj = getSecureConnection()
        cursorObj.execute("drop table if exists {}".format(tableName))
    except Exception as inst:
        print(type(inst))
        print(inst)
        input("> ")
    finally:
        dbObj.commit()
        closeConnection(dbObj, cursorObj)
        print("Table dropped successfully")
    return

def testStatement():
    print("TEST:")
    dbObj, cursorObj = getConnection()

    uid = '647'
    picid = 'P01'
    if uid == '' and picid == '':
        statement = "select * from photos"
        cursorObj.execute(statement)
    elif uid == '' and picid != '':
        statement = "select * from photos where picid = %s"
        cursorObj.execute(statement,(picid,))
    elif uid != '' and picid == '':
        statement = "select * from photos where uid=%s"
        cursorObj.execute(statement, (uid,))
    elif uid != '' and picid != '':
        statement = "select * from photos where uid = %s and picid = %s"
        cursorObj.execute(statement, (uid,picid))
    tables = cursorObj.fetchall()
    print("Results:\n{}".format(tables))

    fileNames = list()

    for tup in tables:
        fname = "{}.{}.{}".format(tup[0], tup[1], tup[2])
        fileNames.append(fname)
        file = open(fname, 'wb').write(tup[3])
        im = Image.open(fname).show()
        os.remove(fname)

    closeConnection(dbObj, cursorObj)
    sys.exit()
    return

def tableHeaders():
    ''' Return the headers of a given table
    Parameters:
        None

    Returns:
        tables (list):  the list of tuples containing the headers
    '''
    tables = list()
    try:
        dbtable = input("input the table you want to view the headers of\n>")
        dbObj, cursorObj = getConnection()
        cursorObj.execute("SELECT column_name FROM information_schema.columns WHERE table_name = %s", (dbtable,))
        tables = cursorObj.fetchall()
    except Exception as inst:
        print(type(inst))
        print(inst)
        input("> ")
    finally:  closeConnection(dbObj, cursorObj)
    return tables

def selectStatement():
    ''' User inputs a select statement from cmd line that the program executes
    Parameters:
        None

    Returns:
        tables (list):  the returned list of tuples containing the returned values
    '''
    print("There are 3 parts: SELECT, FROM, WHERE")
    sel = input("input the SELECT part\n>")
    frm = input("input the FROM part\n>")
    whr = input("input the WHERE part\n>")
    tables = list()
    try:
        dbObj, cursorObj = getConnection()
        if whr == '':
            cursorObj.execute("select {} from {}".format(sel, frm))
        else:
            cursorObj.execute("select {} from {} where {}".format(sel, frm, whr))
        tables = cursorObj.fetchall()
    except Exception as inst:
        print(type(inst))
        print(inst)
        input("> ")
    finally:  closeConnection(dbObj, cursorObj)
    return tables

def selectPhotos():
    ''' TODO: Break into smaller functions
    '''
    try:
        dbObj, cursorObj = getConnection()
        uid = input("Please enter the uid:\n>")
        picid = input("Please enter the picture id:\n> ")
        if uid == '' and picid == '':
            statement = "select * from photos"
            cursorObj.execute(statement)
        elif uid == '' and picid != '':
            statement = "select * from photos where picid = %s"
            cursorObj.execute(statement,(picid,))
        elif uid != '' and picid == '':
            statement = "select * from photos where uid=%s"
            cursorObj.execute(statement, (uid,))
        elif uid != '' and picid != '':
            statement = "select * from photos where uid = %s and picid = %s"
            cursorObj.execute(statement, (uid,picid))
        tables = cursorObj.fetchall()
        pause = input("Would you like to pause after each picture? y/n\n> ")
        for tup in tables:
            fname = "{}.{}.{}".format(tup[0], tup[1], tup[2])
            file = open(fname, 'wb').write(tup[3])
            im = Image.open(fname).show()
            os.remove(fname)
            if pause == 'y': input(">")
    except Exception as inst:
        print(type(inst))
        print(inst)
        input("> ")
    finally:  closeConnection(dbObj, cursorObj)
    return

def viewTables():
    ''' View all the tables in the current database
    Parameters:
        None

    Returns:
        returnList (list):  list of the returned tuples
    '''
    returnList = list()
    try:
        dbObj, cursorObj = getConnection()
        cursorObj.execute('SELECT tablename FROM pg_catalog.pg_tables;')
        tables = cursorObj.fetchall()
        for tuple in tables:
            for entry in tuple:
                if not ("pg_" in entry or "sql_" in entry): returnList.append(entry)
    finally:  closeConnection(dbObj, cursorObj)
    return returnList

def mainmenu():
    ''' Print the main menu of options available to the user
    Parameters:
        None

    Returns:
        None
    '''
    print("\nWhat do you want to do? Options:")
    print("(vat) view all tables, (ss) sql select, (sp) select photo, (th) table headers, (q) quit")
    choice = ''
    while choice != 'q':
        choice = input("\nWhat do you want to do?\n> ")
        if choice == 'vat':
            res = viewTables()
            printResults(res)
        elif choice == 'ss':
            res = selectStatement()
            printResults(res)
        elif choice == 'th':
            res = tableHeaders()
            printResults(res)
        elif choice == 'sp':
            selectPhotos()
        elif choice == 'sql':
            sqlStatement()
    return

def printResults(tup):
    ''' Print whatever is passed in the parameters
    Parameters:
        tup (list)      hopefully a list or tuple to print (or anything else)

    Returns:
        None
    '''
    print("Results:\n{}".format(tup))
    return

def sqlStatement():
    try:
        dbObj, cursorObj = getSecureConnection()
        print("Enter your sql statement and hit enter when done")
        statement = input("> ")
        cursorObj.execute(statement)
        tables = cursorObj.fetchall()
        print("Results:\n{}".format(tables))
    except Exception as inst:
        print(type(inst))
        print(inst)
        input("> ")
    finally:  closeConnection(dbObj, cursorObj)
    return

def main():
    executeArgs()
    mainmenu()
    return

if __name__ == '__main__':
    main()
