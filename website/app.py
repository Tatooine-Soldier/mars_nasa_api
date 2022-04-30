from re import U
from flask import Flask, render_template
import requests
from urllib.request import urlretrieve
from pprint import PrettyPrinter, pprint
import json

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
    final_temp_dict = {}
    final_wind_dict = {}
    final_dict = {} #put both dictionaries in this dictionary
    #print(yearlist)
    i = 0
    while i < 6:
        yr = yearlist[i]
        # print("Average temperature on Mars on sol {} was {}".format(yearlist[i],marsdata[yr]['AT']['av']))
        my_list = [marsdata[yr]['AT']['av'], marsdata[yr]['HWS']['av']]
        final_dict[yearlist[i]] = my_list
        # final_temp_dict[yearlist[i]] = marsdata[yr]['AT']['av']
        # final_wind_dict[yearlist[i]] = marsdata[yr]['HWS']['av']
        i = i+1
    # final_dict["temperature"] = final_temp_dict
    # final_dict["wind"] = final_wind_dict
    return final_dict

# def getAvgWs(marsdata, yearlist):
#     ws_list = []
#     i = 0
#     while i < 6:

#         ws_list.append()




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

