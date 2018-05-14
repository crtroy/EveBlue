import csv
import sqlite3
import pandas

pandas.set_option('display.max_rows', 5000)
conn = sqlite3.connect("arms.db")
c = conn.cursor()

tableCount = 3

#############################################################################
#########################   Creating Tables    ##############################
#############################################################################
# Create tables and check for errors.
# Pull table names
temp = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
# Add data to tables if tables are not present
tableNames = []
# Add table names to array
for name in temp:
    tableNames.append(name[0])

# Check to see if correct number of table are present
if not len(tableNames) == tableCount:
    # Check to see if DB is empty
    # If not, remove existing tables
    if not len(tableNames) == 0:
        for i in range(0, len(tableNames)):
            c.execute("DROP TABLE IF EXISTS tableNames[i]")

    # Create table blueprintIDs
    c.execute('''CREATE TABLE IF NOT EXISTS blueprintIDs
        (typeID text, maxProductionLimit text)''')
    reader = csv.reader(open('industryBlueprints.csv', 'r'))
    for row in reader:
        to_db = [(row[0]), (row[1])]
        c.execute("INSERT INTO blueprintIDs VALUES (?, ?)", to_db)

    # Create table itemList
    c.execute('''CREATE TABLE IF NOT EXISTS itemList
        (typeID text, groupID text, typeName text)''')
    reader = csv.reader(open('invTypes.csv', encoding="utf8"))
    for row in reader:
        to_db = [(row[0]), (row[1]), (row[2])]
        c.execute("INSERT INTO itemList VALUES (?, ?, ?)", to_db)

    # Create table materialList
    c.execute('''CREATE TABLE IF NOT EXISTS materialList
        (typeID text, activityID text, materialTypeID text, quantity text)''')
    reader = csv.reader(open('industryActivityMaterials.csv', 'r'))
    for row in reader:
        to_db = [(row[0]), (row[1]), (row[2]), (row[3])]
        c.execute("INSERT INTO materialList VALUES (?, ?, ?, ?)", to_db)

#############################################################################


while 1:
	print("\ntype 1 for blueprint search")
	print("type 2 for materials required")
	print("type 3 to exit")
	choice = int(input())
	if choice == 1:
		print("Enter name to be searched")
		sminer = input()
		# Display exact result only
		searched = pandas.read_sql_query("SELECT typeName FROM itemList WHERE typeName LIKE '%"+sminer+"%Blueprint'", conn)
		print(searched)
		
	elif choice == 2:
		print("Enter blueprint name (exclude Blueprint)\n")
		sminer = input()
		# Display all results containing user input
		allMats = pandas.read_sql_query(
		"SELECT typeName, quantity FROM itemList A INNER JOIN("
			"SELECT * FROM materialList WHERE activityID = '1' AND typeID IN("
				"SELECT typeID FROM itemList WHERE typeName = '"+sminer+" Blueprint'"
					")) B WHERE A.typeID = B.materialTypeID", conn)
		print(allMats)

	elif choice == 3:
		print("Exiting\n")
		break
	else:
	    print("Invalid Selection\n")

conn.commit()
conn.close()