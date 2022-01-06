import os
import pandas as pd

image_list = []

    # DO NOT USE absolut path
    #source_images_folder = "C:\\PWPproject\\ImageAnnotator\\data\\ImageTest\\"
    # USE relative path
cwd = os.getcwd()
folder = '\\data\\'
csv_file = 'HS_ALL_TEST_SET.xlsx'
csv_source = cwd + folder + csv_file
print(csv_source)

data= pd.read_excel(csv_source)
column_names = data.columns

testRows = pd.read_excel(csv_source, nrows=10)

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