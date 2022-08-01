import sqlite3
con = sqlite3.connect('db.sqlite3')

cur = con.cursor()
vaseRef = 16
collectionName = "Blah"
params = (vaseRef, collectionName)
test = cur.execute('SELECT * FROM website_vase')
print(test)

for x in test:
    print(x)