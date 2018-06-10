# Copyright © 2018 Troy Coats
# This work is available under the "MIT License".
# Please see the file LICENSE in this distribution
# for license terms.

import os
import csv
import sqlite3

conn = sqlite3.connect("data/blueprints.db")
c = conn.cursor()
tableCount = 3

# Pull existing table names from database
temp = conn.execute("""SELECT name
                       FROM sqlite_master
                       WHERE type='table'""")

# Add table names to array
# Table 1 = itemList
# Table 2 = materialList
# Table 3 = buildTimes
tableNames = []
for name in temp:
    tableNames.append(name[0])
    
# Check to see if correct number of table are present
# If not then DB will be created from csv files
if not len(tableNames) == tableCount:
    # Check to see if DB is empty
    # If not, disconnect from db, delete db, reconnect to db
    if not len(tableNames) == 0:
        conn.close()
        os.remove("data/blueprints.db")
        conn = sqlite3.connect("data/blueprints.db")
        c = conn.cursor()
    
    # Create table itemList
    # Column 1 = typeID
    # Column 2 = groupID
    # Column 3 = typeName
    c.execute("""CREATE TABLE IF NOT EXISTS itemList
        (typeID text, groupID text, typeName text)""")
    reader = csv.reader(open('data/invTypes.csv', encoding="utf8"))
    for row in reader:
        to_db = [(row[0]), (row[1]), (row[2])]
        c.execute("""INSERT INTO itemList
                     VALUES (?, ?, ?)""", to_db)

    # Create table materialList
    # Column 1 = typeID
    # Column 2 = materialTypeID
    # Column 3 = quantity
    c.execute("""CREATE TABLE IF NOT EXISTS materialList
        (typeID text, materialTypeID text, quantity text)""")
    reader = csv.reader(open('data/industryActivityMaterials.csv', 'r'))
    for row in reader:
        if row[1] == '1':    
            to_db = [(row[0]), (row[2]), (row[3])]
            c.execute("""INSERT INTO materialList
                         VALUES (?, ?, ?)""", to_db)

    # Create table timeList
    # Column 1 = typeID
    # Column 2 = time
    c.execute("""CREATE TABLE IF NOT EXISTS timeList
        (typeID text, time integer)""")
    reader = csv.reader(open('data/industryActivity.csv', 'r'))
    for row in reader:
        if row[1] == '1':
            to_db = [(row[0]), (row[2])]
            c.execute("""INSERT INTO timeList
                         VALUES (?, ?)""", to_db)                     
                     
                     
conn.commit()
conn.close()