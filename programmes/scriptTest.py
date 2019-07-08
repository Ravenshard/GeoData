import os, re, sys, time, unicodedata, math, csv, collections, locale
import psycopg2

def getConnection():
    ''' Connect to the database and return connection and cursor
    Parameters:
        None

    Returns:
        connection:     connection to the database
        cursor:         cursor to be used with the database
    '''
    connect_str = "dbname='test' user='Jay' host='localhost' " + \
                  "password='inriaTravail19'"
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

def main():
    try:
        conn, cursor = getConnection()
        statement = sys.argv[1]
        cursor.execute(open(statement, "r").read())
    except Exception as inst:
        print(type(inst))
        print(inst)
    finally:
        conn.commit()
        closeConnection(conn, cursor)

    print("Success?")
    return


if __name__ == '__main__':
    main()
