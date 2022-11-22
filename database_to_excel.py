# Meria's Annotator for Social Media Texts
# University of Oulu
# Created by Merja Kreivi-Kauppinen (2021-2022)

# transfer database to excel - excel code snippets

#-------------------------------------------#

import json
import os
import re
import sys
import sqlite3
from openpyxl import load_workbook
import xlsxwriter 

#----------- Open SQLite connection and Print SQL table as rows  ----------------

conn = sqlite3.connect('developmentHateSpeech.db')
print('\nOpened SQL database successfully')
c = conn.cursor()

print('\nPrint SQL table as rows\n')

collectedComments = []

def sql_fetch(conn):
    c = conn.cursor()
    c.execute('SELECT * FROM YouTubeComsCollection')
    rows = c.fetchall()
    for row in rows:
        print(row)
        collectedComments.append(row)
sql_fetch(conn)

conn.close()
print("\nSQL table printed successfully and closed\n")

# ---------------------------------------------------------
# Amount of rows
print('\nAmount of rows:', len(collectedComments), '\n')

"""
# --------------------------------------------------------
# clean urls because of excel limits

split_comments = []
for item in collectedComments:
    split_comments.append(item.split())

cleaned_https = []
for comment in split_comments:
    
    cleaned_word_list = []
    for single_word in comment:
        regex = re.compile('(https?:\/\/)(\s)*(www\.)?(\s)*((\w|\s)+\.)*([\w\-\s]+\/)*([\w\-]+)((\?)?[\w\s]*=\s*[\w\%&]*)*')
        #regex = re.compile('[\W+]')
        #First parameter is the replacement, second parameter is your input string
        nonAlphaRemoved = regex.sub('', single_word)
        # add string to list only if it has content
        if nonAlphaRemoved:
            cleaned_word_list.append(nonAlphaRemoved)
    
    cleaned_https.append(cleaned_word_list)


#------------------- JOIN -------------------------#

#comments_list = []
#for comment in cleaned_https:
#    sentences = []

comments_list = (" ".join(item) for item in (cleaned_https))

#    comments_list.append(sentences)

print('\nJoined comments:', '\n')
print(comments_list)
"""


# ------------------- xlsxwriter ------------------------------
# xlsx -workbook located in the same folder as this code

MyWorkbook = xlsxwriter.Workbook('YouTubeComments.xlsx') 
MyWorksheet = MyWorkbook.add_worksheet("YouTubeComments") 

# Start from the first cell. Rows and columns are zero indexed. 
row = 1
column = 0

# testing
#content = ["ankit", "rahul", "priya", "harshita", "sumit", "neeraj", "shivam"] 

# iterating through content list 
for sentence in collectedComments: 
    # write operation perform 
    MyWorksheet.write(row, column, sentence[0])
    # incrementing the value of row by one with each iteratons
    row += 1
MyWorkbook.close()
