# Copyright © 2018 Troy Coats
# This work is available under the "MIT License".
# Please see the file LICENSE in this distribution
# for license terms.

from tkinter import *
import sqlite3

from ctypes import windll, byref, create_unicode_buffer, create_string_buffer
FR_PRIVATE  = 0x10
FR_NOT_ENUM = 0x20

##################################################################################################
##########          Functions       ##############################################################
##################################################################################################

# Function to load custom font
# This function was taken from:
# https://stackoverflow.com/questions/11993290/truly-custom-font-in-tkinter/30631309#30631309
def loadfont(fontpath, private=True, enumerable=False):
    if isinstance(fontpath, bytes):
        pathbuf = create_string_buffer(fontpath)
        AddFontResourceEx = windll.gdi32.AddFontResourceExA
    elif isinstance(fontpath, str):
        pathbuf = create_unicode_buffer(fontpath)
        AddFontResourceEx = windll.gdi32.AddFontResourceExW
    else:
        raise TypeError('fontpath must be of type str or unicode')

    flags = (FR_PRIVATE if private else 0) | (FR_NOT_ENUM if not enumerable else 0)
    numFontsAdded = AddFontResourceEx(byref(pathbuf), flags, 0)
    return bool(numFontsAdded)

# Clear/reset lists
def resetTables(conn):
    blueprintList.delete('0','end')
    nameText.config(state='normal')
    nameText.delete('1.0','end')      
    timeList.delete('0','end') 
    materialList.delete('0','end')
    quantityList.delete('0','end')
    nameText.config(height=1)
    timeList.config(height=1)
    materialList.config(height=1)
    quantityList.config(height=1)
    nameText.insert('end', 'No Blueprint Selected', 'justify')
    nameText.config(bg='#707070', selectbackground='#707070', state='disabled')   
    timeList.insert('end', 'No Blueprint Selected')
    materialList.insert('end', 'No Blueprint Selected')
    quantityList.insert('end', '00000000')

# Calculate build time
def buildTime(time):
    if time == 0:
        return "Instant"
    else:
        days = int(time / 86400)
        hours = int((time - 86400 * days) / 3600)
        minutes = int(((time - 86400 * days) - (3600 * hours)) / 60)
        seconds = int(((time - 86400 * days) - (3600 * hours)) - (60 * minutes))
        if days > 0:
            totalTime = str(days) + " day"
            if days > 1:
                totalTime = totalTime + "s"
        if hours > 0:
            if days > 0:
                totalTime = totalTime + ", " + str(hours) + " hour"
            else:
                totalTime = str(hours) + " hour"
            if hours > 1:
                totalTime = totalTime + "s"
        if minutes > 0:
            if days > 0 or hours > 0:
                totalTime = totalTime + ", " + str(minutes) + " minute"
            else:
                totalTime = str(minutes) + " minute"
            if minutes > 1:
                totalTime = totalTime + "s"
        if seconds > 0:
            if days > 0 or hours > 0 or minutes > 0:
                totalTime = totalTime + ", " + str(seconds) + " second"
            else:
                totalTime = str(seconds) + " second"
            if seconds > 1:
                totalTime = totalTime + "s"
        return totalTime 
   
# Populate lists with new data    
def populateBlueprints():
    resetTables(conn)
    searchBar.delete('0', 'end')
    c.execute("""SELECT DISTINCT A.typeName
                 FROM itemList A, materialList B
                 WHERE A.typeID = B.typeID AND A.typeName LIKE '%Blueprint'
                 ORDER BY A.typeName""")
    # Insert data and set list colors
    for row in c:
        blueprintList.insert('end', row[0])
    for i in range(0,blueprintList.size(),2):
        blueprintList.itemconfigure(i, bg='#707070')
    for i in range(1,blueprintList.size(),2):   
        blueprintList.itemconfigure(i, bg='#808080')
    
    blueprintList.configure(height=22)
    scrollbar.grid(padx=440, pady=168, row=0,column=0, ipady=405)

# Search DB for blueprint based on user input    
def searchForBlueprint():
    resetTables(conn)
    result = searchBar.get()
	# Display exact result only
    c.execute("""SELECT *
                 FROM(
                    SELECT DISTINCT A.typeName
                    FROM itemList A, materialList B
                    WHERE A.typeID = B.typeID AND A.typeName LIKE '%Blueprint'
                    ORDER BY A.typeName
                 )
                 WHERE typeName LIKE ?""", ('%'+result+'%',))               
    # Insert data and set list colors
    for row in c:
        blueprintList.insert('end', row[0])
    for i in range(0,blueprintList.size(),2):
        blueprintList.itemconfigure(i, bg='#707070')
    for i in range(1,blueprintList.size(),2):   
        blueprintList.itemconfigure(i, bg='#808080') 
    
    # If no results were returned    
    if blueprintList.size() == 0:
        blueprintList.config(height=1)
        blueprintList.insert('end', "Search returned no results")
        scrollbar.grid_forget()
    # If more than 22 results were returned       
    elif blueprintList.size() < 22:
        blueprintList.configure(height=blueprintList.size())
        scrollbar.grid_forget()
    # If less than 22 results were returned    
    else:
        blueprintList.configure(height=22)
        scrollbar.grid(padx=440, pady=168, row=0,column=0, ipady=405)
        
# Function to populate material and material count blueprintListes
# This function is called every time a line in the blueprint
# blueprintList is selected, whether it is by mouseclick or arrow key.
def CurrentSelection(event):
    widget = event.widget
    # Check to see if listBox was set to empty
    if blueprintList.get(0,0) != ('Search returned no results',):
        selected = widget.get(widget.curselection()[0])  
        
        # Output name of selected blueprint
        nameText.config(state='normal')        
        nameText.delete('1.0', 'end')
        nameText.insert('end', selected, 'justify')
        nameText.config(bg='#454575', selectbackground='#454575', state='disabled')
        
        # Delete old values from materials and quantity listBoxes
        timeList.delete('0','end')        
        materialList.delete('0','end')
        quantityList.delete('0','end')
        
        # Insert time into the time list
        c.execute("""SELECT time
                            FROM timeList A INNER JOIN(
                                SELECT typeID
                                FROM itemList
                                WHERE typeName = ?
                            ) B
                            WHERE A.typeID = B.typeID""", [selected])
        for row in c:
            time = row[0]
        timeList.insert('end', buildTime(time))
 
         # Insert materials and quantities into respective listBoxes
        c.execute("""SELECT typeName, quantity, A.typeID
                     FROM itemList A INNER JOIN(
                         SELECT *
                         FROM materialList
                         WHERE typeID IN(
                             SELECT typeID
                             FROM itemList
                             WHERE typeName = ?
                         )
                     ) B
                     WHERE A.typeID = B.materialTypeID""", [selected])  
        for row in c:
            materialList.insert('end', row[0])
            quantityList.insert('end', row[1])
            
        # Set size of materials and quantity listBoxes based on number retrieved
        materialList.config(height=materialList.size())
        quantityList.config(height=quantityList.size())
        
        # Create alternating background colors for materials and quantity listBoxes
        # Based on new listBox size
        for i in range(0,materialList.size(),2):
            materialList.itemconfigure(i, bg='#707070')
        for i in range(1,materialList.size(),2):   
            materialList.itemconfigure(i, bg='#808080')
        for i in range(0,materialList.size()):   
            materialList.itemconfigure(i, {'fg': '#ffffff'})      
        for i in range(0,quantityList.size(),2):
            quantityList.itemconfigure(i, bg='#707070')
        for i in range(1,quantityList.size(),2):   
            quantityList.itemconfigure(i, bg='#808080')
        for i in range(0,quantityList.size()):   
            quantityList.itemconfigure(i, {'fg': '#ffffff'})


##################################################################################################
##########          Body       ###################################################################
##################################################################################################
        
# Load "Eve Alpha" font      
loadfont("data/eve.ttf")
        
# Connect to blueprints.db
conn = sqlite3.connect("data/blueprints.db")
c = conn.cursor()

# Create main window
window = Tk()
window.title("Eve Blue")
window.minsize(width=1200, height=1080)
window.maxsize(width=1200, height=1080)

# Setup background image
backgroundImage = PhotoImage(file="data/eve.png")
backgroundLabel = Label(image=backgroundImage)
backgroundLabel.place(x=-600, y=0, relheight=1)

# Create/place search bar
searchBar = Entry(bd=4, width=47, selectforeground="#ffffff",insertbackground='#ff4500')
searchBar.configure(bg="#404040", fg="#ffffff", font=("Helvetica", 12))
searchBar.place(x=10, y=50)

# Create/place Labels
searchbarHeader = Label(font=("eve alpha", 14), text="Bluprint Search")
blueprintHeader = Label(font=("eve alpha", 14), text="Bluprint Name")
timeHeader = Label(font=("eve alpha", 14), text="Build Time")
materialHeader = Label(font=("eve alpha", 14), text="Materials")
quantityHeader = Label(font=("eve alpha", 14), text="Quantity")
searchbarHeader.place(x=10, y=10)
blueprintHeader.place(x=10, y=128)
timeHeader.place(x=480, y=168)
materialHeader.place(x=480, y=268)
quantityHeader.place(x=915, y=268)

# Create scrollbar
scrollbar = Scrollbar(orient="vertical")

# Create name Text
nameText = Text(fg="#ffffff", bg = "#454577", width=67, relief='raised')
nameText.configure(borderwidth=10, selectbackground='#454575', font=("Helvetica", 12), exportselection=0)
nameText.tag_configure('justify', justify='center')
nameText.place(x=480, y=118)

# Create/place listboxes
blueprintList = Listbox(fg="#ffffff", bg = "#707070", height=22, width=45, exportselection=0)
blueprintList.configure(selectborderwidth=10, selectbackground='#454577', font=("Helvetica", 12))
blueprintList.configure(yscrollcommand=scrollbar.set)
timeList = Listbox(fg="#ffffff", bg = "#707070", width=45)
timeList.configure(selectborderwidth=10, selectbackground='#707070', font=("Helvetica", 12), exportselection=0)
materialList = Listbox(fg="#ffffff", bg = "#707070", width=45)
materialList.configure(selectborderwidth=10, selectbackground='#707070', font=("Helvetica", 12), exportselection=0)
quantityList = Listbox(fg="#ffffff", bg = "#707070", width=18)
quantityList.configure(selectborderwidth=10, selectbackground='#707070', font=("Helvetica", 12), exportselection=0)
blueprintList.place(x=10, y=168)

timeList.place(x=480, y=208)
materialList.place(x=480, y=308)
quantityList.place(x=915, y=308)

# Create/place search bar buttons
searchButton = Button(window, highlightcolor="#ff5400", text="Search", font=("eve alpha", 11))
searchButton.configure(command=searchForBlueprint)
searchBar.bind("<Return>", lambda event: searchForBlueprint())
clearButton = Button(text="Clear", font=("eve alpha", 11))
clearButton.configure(command=populateBlueprints)
searchButton.place(x=480, y=50)
clearButton.place(x=610, y=50)

# Populate list: blueprintList
populateBlueprints()

# Call CurrentSelection function
blueprintList.bind("<<ListboxSelect>>", CurrentSelection)

# Attach scrollbar to blueprintList Listbox
scrollbar.config(command=blueprintList.yview)

# Set tab order of widgets
order = (searchBar, searchButton, clearButton, blueprintList, materialList, quantityList)
for widget in order:
    widget.lift()


# Run main loop
window.mainloop()
# Close database
conn.close()
