'''
    HOW TO ADD IMAGES TO DATABASE:
    run program as follows:
        python .\programmes\readdata.py -apf .\photos
    It will take some time, but it should say 'Photos added successfully'
    after some time.  After you can hit 'q' to quit, and all is good.

    IL FAUT QU'ON TÉLÉCHARGE "pillow" et "psycopg2" POUR UTILISER CE DOSSIER
    - pip install pillow  <-- c'est tout pour installer "pillow"
    - pip install psycopg2 <-- c'est tout pour installer "psycopg2"

'''

import sys, psycopg2
from PIL import Image

user = "Jay"
dbname = "ecrains"

def getConnection():
    ''' Se connecter à la base de données et revenir le "connection" et le "cursor"
    Paramètres:
        Null

    Résultats:
        connection:     connection à la base de données
        cursor:         cursor utiliser avec la base de données
    '''
    global user, dbname
    connect_str = "dbname='{}' user='{}' host='localhost' ".format(dbname, user) + \
                  "password='inriaTravail19'"
    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()
    return (conn, cursor)

def getSecureConnection():
    ''' Se connecter à la base de données et revenir le "connection" et le "cursor"
    Paramètres:
        Null

    Résultats:
        connection:     connection à la base de données
        cursor:         cursor utiliser avec la base de données
    '''
    global user, dbname
    pw = input("saisez le mot de passe:\n> ")
    connect_str = "dbname='{}' user='{}' host='localhost' ".format(dbname, user) + \
                  "password='{}'".format(pw)
    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()
    return (conn, cursor)

def closeConnection(conn, cursor):
    ''' Fermer la connexion avec la base de données
    Paramètres:
        conn:       connection à fermer
        cursor:     cursor à fermer

    Résultats:
        Null
    '''
    cursor.close()
    conn.close()
    return

def executeArgs():
    ''' Exécuter tous les arguments depuis la ligne de commande avant d'exécuter le programme
    parameters:
        Null

    Résultats:
        Null
    '''
    index = 1
    while index < len(sys.argv):
        if sys.argv[index] == '-apf':
            index +=1
            if os.path.exists(sys.argv[index]):  addPhotoFile(sys.argv[index])
        index += 1
    return

def addPhotoFile(file):
    ''' Adjouter des photos à la base de données
    parameters:
        Null

    Résultats:
        Null
    '''
    try:
        allPhotos = os.listdir(file)
        dbObj, cursorObj = getSecureConnection()
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
        print("Des photos ont adjouté avec succès")
    return

def queryPhoto(dbObj, cursorObj):
    ''' Prendre des entrées et faire une requête
    Paramètres:
        dbObj:       connection à la base de données
        cursorObj:   cursor à pour la base de données

    Résultats:
        Null
    '''
    uid = input("saisez l'uid:\n>")
    picid = input("saisez l'id de photo:\n> ")
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
    return

def selectPhotos():
    ''' Sélectionner des photos pour revenir à l'utiliseur
    parameters:
        Null

    Résultats:
        Null
    '''
    try:
        dbObj, cursorObj = getConnection()
        queryPhoto(dbObj, cursorObj)
        tables = cursorObj.fetchall()
        pause = input("Vous voudrais faire une pause après chaque photo?  o/n\n> ")
        for tup in tables:
            fname = "{}.{}.{}".format(tup[0], tup[1], tup[2])
            file = open(fname, 'wb').write(tup[3])
            im = Image.open(fname).show()
            os.remove(fname)
            if pause == 'o': input(">")
    except Exception as inst:
        print(type(inst))
        print(inst)
        input("> ")
    finally:  closeConnection(dbObj, cursorObj)
    return

def mainmenu():
    ''' Commencer tout, l'utilisateur peut sélectionner des photos
    Paramètres:
        Null

    Résultats:
        Null
    '''
    choice = input("taper 'q' pour quitter la programme ou autre chose pour continuer et sélectionner des photos \n> ")
    while choice != 'q':
        selectPhotos()
        choice = input("taper 'q' pour quitter la programme ou autre chose pour continuer et sélectionner des photos \n> ")
    return

def main():
    executeArgs()
    mainmenu()
    return

if __name__ == '__main__':
    main()
