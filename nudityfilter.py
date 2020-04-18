#CREDITS: DeepAI.org for providing documentation and this useful API | RaresJ.ro for showing you how it works and how to export relevant data in csv format

import requests
import os
import json
import csv

API_KEY = "quickstart-QUdJIGlzIGNvbWluZy4uLi4K" #enter your API key from DeepAI.org | This key is the free one from the documentation and you can use it for 5requests

def scanLocalImg(path):
    r = requests.post(
        "https://api.deepai.org/api/nsfw-detector",
        files={
            'image': open(path, 'rb'),
        },
        headers={'api-key': API_KEY}
    )
    return r.json() #returns the json response as a dict

def export_csv(csv_filename,inputData):
    keys = inputData[0].keys()
    with open(csv_filename, 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(inputData)

importedPhotosList = os.listdir('./import') #list all imported items

outputList = [] #define output list

for item in importedPhotosList:
    jsonResponseDict = scanLocalImg('./import/'+item)
    detectionData = jsonResponseDict["output"]["detections"]
    detectionData = detectionData[0] #The relevant data comes inside a list for some reason but as far as I know we cannot do a multiple-images upload

    #You can use print(detectionData) 

    if len(detectionData["name"]) != 0:
        detectionData["body_part_name"] = detectionData["name"].split("-")[0]
        detectionData["body_part_visibility"] = detectionData["name"].split("-")[1]
    else:
        detectionData["body_part_name"] = ""
        detectionData["body_part_visibility"] = ""

    #detectionData["path"] = "./import/"+item
    detectionData["img_name"] = item
    
    del detectionData["bounding_box"]
    del detectionData["name"]
    outputList.append(detectionData)

export_csv("export.csv", outputList) #export to csv

