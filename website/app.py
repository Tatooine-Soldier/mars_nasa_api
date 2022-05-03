from re import U
from flask import Flask, render_template
import requests
from urllib.request import urlretrieve
from pprint import PrettyPrinter, pprint
import json
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt 
import csv

pp = PrettyPrinter()

app = Flask(__name__)

api_key = 'HHzOZfKZgwxrajynxldzhmLvt2SjTlU0OkzS81yA'

@app.route("/")
def main():

    resp = fetchMarsData()
    print(resp)
    #str(resp)
    return render_template("home.html", sols=resp)
    # resp = fetchAsteroidNeowsFeed()
    # return "<p>{}</p>".format(resp)

@app.route("/iss")
def main_iss():
    data = getISS()
    print(data)
    return render_template("iss.html", iss_data=data)

def fetchMarsData():
    URL_MarsFeed = "https://mars.nasa.gov/rss/api/?feed=weather&category=insight_temperature&feedtype=json&ver=1.0"
    response = requests.get(URL_MarsFeed).json()
    pprint(response)
    with open("mars_weather_info.json", "w") as file_object:
        json.dump(response, file_object)
    with open("mars_weather_info.json","r") as file_object:  
        data = json.load(file_object)  #returns a dictionary
    # print(data['675']['AT']['av'])
    list_of_years = []
    for year in data:
        list_of_years.append(year)
    return getAvgTemp(data, list_of_years)
    
        
def getAvgTemp(marsdata, yearlist):
    final_dict = {} #put both dictionaries in this dictionary
    #print(yearlist)
    i = 0
    while i < 6:
        yr = yearlist[i]
        # print("Average temperature on Mars on sol {} was {}".format(yearlist[i],marsdata[yr]['AT']['av']))
        my_list = [marsdata[yr]['AT']['av'], marsdata[yr]['HWS']['av']]
        final_dict[yearlist[i]] = my_list
        i = i+1
    return final_dict


def getISS():
    URL_ISSFeed = "http://api.open-notify.org/iss-now.json"
    response = requests.get(URL_ISSFeed).json()
    with open("ISS_data.json", "w") as file_object:
        json.dump(response, file_object)
    with open("ISS_data.json","r") as file_object:  
        data = json.load(file_object)
    stamp = data["timestamp"]
    stamp_time = datetime.utcfromtimestamp(stamp).strftime('%Y-%m-%d %H:%M:%S')
    isscsv_list = [] #coords passed into csv gile
    iss_dict = {}
    iss_dict[stamp_time] = data
    for kdate,item in iss_dict.items():
        isscsv_list.append(item["iss_position"]["latitude"])
        isscsv_list.append(item["iss_position"]["longitude"])
    with open('iss_data.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(isscsv_list)
    return iss_dict


# def issLocation():
#     df = pd.read_csv('iss_data.csv')



# def fetchAsteroidNeowsFeed():
#     print("calling")
#     URL_NeoFeed = "https://api.nasa.gov/neo/rest/v1/feed"
#     params = {
#         'api_key':api_key,
#         'start_date':'2022-03-22',
#         'end_date':'2022-03-23'
#     }
#     response = requests.get(URL_NeoFeed,params=params).json()
#     pp.pprint(response)
#     response_not_string = response
#     filename = "asteroid_info.json"
#     with open(filename, 'w') as file_object:  #open the file in write mode
#         json.dump(response_not_string, file_object)
#     readAsteroidJSONfile("asteroid_info.json")
#     return str(response)

# def readAsteroidJSONfile(file):
#     with open(file,"r") as file_object:  
#         data = json.load(file_object)  #returns a dictionary
#         #data[][]<-- query it like this, nested dictionary
#         print(data["near_earth_objects"]["2022-03-22"])
#         neo_list = data["near_earth_objects"]["2022-03-22"]
#         absolute_magnitude = neo_list[0]["absolute_magnitude_h"]
#         print("\n** {} **\n".format(absolute_magnitude)) 

