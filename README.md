# EveBlue
Copyright (c) 2018 Troy Coats

EveBlue is a simple program to view EVE Online blueprints and the materials required to create them.

The initial goal of this project was to learn a little bit about Python and GUI development.
This tool was written in Python3 using Tkinter and sqlite3. 

## Usage
Setup is pretty straight forward. Just run the file **eveBlue.py**.

If Database needs to be updated (or created for some reason) just make sure the files **invTypes.csv**, **industryActivityMaterials.csv**, and **industryActivity.csv** are in the **data** folder and run **createDB.py**.
=======
If Database needs to be updated (or created for some reason) just make sure the files **invTypes.csv**, **industryActivityMaterials.csv**, and **industryActivity.csv**are in the **data** folder and run **createDB.py**.

This program has only been tested using Python3 on Windows 10.

## License
This work is licensed under the "MIT License". Please see the file LICENSE in the source distribution of this software for license terms.

## Acknowledgements/Sources
Files for the database were found at:
<br>&nbsp;&nbsp;&nbsp;&nbsp;https://www.fuzzwork.co.uk/dump/latest/
<br>Custom font function taken from stack overflow:
<br>&nbsp;&nbsp;&nbsp;&nbsp;https://stackoverflow.com/questions/11993290/truly-custom-font-in-tkinter/30631309#30631309
<br>Eve custom font "Eve Alpha" from author Damián Vila can be found at:
<br>&nbsp;&nbsp;&nbsp;&nbsp;http://eve.damianvila.com/fonts.htm
<br>Background image taken from CCP Games promotional material.
