# Meria's Annotator for Social Media Texts
# University of Oulu
# Created by Merja Kreivi-Kauppinen (2021-2022)

# Social-Media-Text-Annotator/HateSpeechAnnotator API

# This file was created for testing purposes

"""
In order to run this test code of ImageAnnotator flask API.

Add following files and folders to ImageAnnotator -folder:

* Data -folder - includes largeTestfile and smallTestfile
* this file 'populate_test_database.py' next to 'manage.py' -file

In order run HateSpeechAnnotator flask API and this file 
activate virtual environment, set flask, init database and populate database.

Activate created python virtual environment (on cmd):
    
    cd C:\GIT\Repositories\Social-Media-Text-Annotator\.venv\Scripts
    activate.bat

Go to ImageAnnotator folder: (provide 'cd ..' on cmd)
    (.venv) C:\GIT\Repositories\Social-Media-Text-Annotator>

Set configuration setting class as 'development' or 'production' or 'default' or 'testing'
    (.venv) C:\GIT\Repositories\Social-Media-Text-Annotator>set FLASK_ENV=development

In order to start the server set the package name 'hub' and run Flask in the hub folder:
    (.venv) C:\GIT\Repositories\Social-Media-Text-Annotator>set FLASK_APP=hub

--------------------
EI tehdä

Init flask database basedir hub:
    (.venv) C:\GIT\Repositories\Social-Media-Text-Annotator>flask init-db
Populate flask database:
    (.venv) C:\GIT\Repositories\Social-Media-Text-Annotator>flask populate-db
--------------------

Run test file by command:
    (.venv) C:\GIT\Repositories\Social-Media-Text-Annotator>python test_read_csv_to_dict.py

--------------------

Run flask local host at http://localhost:5000/admin/

    (.venv) C:\GIT\Repositories\Social-Media-Text-Annotator>flask run

TESTING
* This code creates database models, 
* and populates User, TextContent, TextAnnotation

RESULTS
* available at the end of the code

"""

# Run test file by command:
#    (.venv) C:\Social-Media-Text-Annotator\HateSpeechAnnotator>python test_read_csv_to_dict.py


# ------------------------------------------------------------------------------------------


import os
import pandas as pd


    # DO NOT USE absolut path
    #source_images_folder = "C:\\GIT\\Social-Media-Text-Annotator\\data\\HS_ALL_TEST_SET\\"
    # USE relative path instead

cwd = os.getcwd()
folder = '\\data\\'
csv_file = 'HS_ALL_TEST_SET.xlsx'
csv_source = cwd + folder + csv_file
print(csv_source)

data= pd.read_excel(csv_source)
column_names = data.columns

testRows = pd.read_excel(csv_source, nrows=50)

dict = testRows.to_dict('index')

print(len(dict))

i = 0
while i < len(dict):
    print(f'{i+1} / {len(dict)} printed \r')
    
    """print(dict[i]["HSoriginalComment"])
    print(dict[i]["HSbinary"])
    print(dict[i]["HSclass"])
    print(dict[i]["HScategory"])
    print(dict[i]["sentencePolarity"])
    print(dict[i]["sentenceEmotionCategory"])
    print(dict[i]["HSinUrbanFinnish"])
    print(dict[i]["HSinFinnish"])
    print('---------------------')"""
    i= i+1



"""for filename in glob.glob(source_images_folder + '*.jpg'):
        #print("\n Print image data filename:  ", filename)
        #filedate = os.path.getctime(filename)

        with open(filename, "rb") as f:
            timestamp = os.path.getctime(filename)
            datetime_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

            thisdict = {
                "name": os.path.basename(filename),
                "publish_date": datetime.fromisoformat(datetime_str),
                "location": save_to_upload(upload, source_images_folder, os.path.basename(filename)),
                "is_private": False,
                "date": datetime.fromisoformat(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            }
        image_list.appen
        d(thisdict)
    return image_list"""