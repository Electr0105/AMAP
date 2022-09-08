import mysql.connector
import os

mydb = mysql.connector.connect(
host = 'amap-1.cp2wavqmovsc.ap-southeast-2.rds.amazonaws.com',
user = os.environ.get('AWS_USER'),
password = os.environ.get('AWS_PASS'),
database ='pythonDB')

cursor = mydb.cursor()

databaseName = "website_vase"

# def resetTableCounter():
#     cursor.execute("ALTER TABLE website_vase AUTO_INCREMENT = " + (str(1)))
#     for x in cursor:
#         print(x)
#     mydb.commit()

def insertToTable(file):
    try:
        linesInFile = file.decode('utf-8').split('\n')
        for line in linesInFile:
            words = line.split(" ")
            text = "INSERT INTO website_vase (collectionName, previousColl, provenanceName, height, diameter) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}');".format(*words)
            cursor.execute(text)
        mydb.commit()
    except Exception as e: print(e)



