import os
import sys
import glob
import shutil
import sqlite3
import json
import time
import csv
from shutil import Error
from flask import *
from copy import copy
from werkzeug.utils import secure_filename

from functions import json_2_db, coordinates_2_txt, quickSort, haversine, BusStops, BusCompanies, export_json, import_json
from sqlcommands import commands

from flask_googlemaps import get_address, get_coordinates, GoogleMaps, Map

#-------------------------------------

'''Initiating instance objects needed'''

stops = BusStops()
companies = BusCompanies("json/bus_services.json")

'''Creating static mrt data for displaying'''

allmrtbusstops = stops.getmrtbusstops(commands["selectfromdatabase"])

'''Creating static bus data for displaying'''

smrt_numberofservices = len(companies.getbusservices("SMRT"))
sbst_numberofservices = len(companies.getbusservices("SBST"))
tts_numberofservices = len(companies.getbusservices("TTS"))
gas_numberofservices = len(companies.getbusservices("GAS"))

smrt_categories = companies.getcategories("SMRT")
sbst_categories = companies.getcategories("SBST")
tts_categories = companies.getcategories("TTS")
gas_categories = companies.getcategories("GAS")

smrt = companies.countcategories(smrt_categories)
sbst = companies.countcategories(sbst_categories)
tts = companies.countcategories(tts_categories)
gas = companies.countcategories(gas_categories)

'''Creating and inserting relevant data from JSON files to Database file'''

# json_2_db('json/bus_routes.json', 'database/main.db', commands["createbusroutestable"], commands["insertbusroutes"])

# json_2_db('json/bus_services.json', 'database/main.db', commands["createbusservicestable"], commands["insertbusservices"])

# json_2_db('json/bus_stops.json', 'database/main.db', commands["createbusstopstable"], commands["insertbusstops"])

'''Start of Flask WebApp'''
app = Flask(__name__, template_folder='templates')
GoogleMaps(app, key="AIzaSyCCvHi1Jn7gDxjrD1QHRZkPEII3Zy34vgU")


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


@app.after_request
def add_header(response):
    response.cache_control.max_age = 0
    return response


@app.route('/', methods=['POST','GET'])
def home():
    return render_template('laobu.html')


@app.route('/getyourlocation', methods=['GET'])
def getyourlocation():
    return render_template('getyourlocation.html')


@app.route('/learnbusfacts', methods=['GET'])
def learnbusfacts():
    return render_template('learnbusfacts.html', gas = gas, gas_len = gas_numberofservices, smrt = smrt, smrt_len = smrt_numberofservices, sbst = sbst, sbst_len = sbst_numberofservices, tts = tts, tts_len = tts_numberofservices)


@app.route('/findabus', methods=['POST'])
def findabus():

    mymap = Map(
                identifier="view-side",
                varname="mymap",
                style="height:720px;width:1100px;margin:0;", # hardcoded!
                lat=37.4419, # hardcoded!
                lng=-122.1419, # hardcoded!
                zoom=15)

    if request.method == "POST":
        print(request.form)
        data = []
        
        if request.form.get("longitude1") and request.form.get("latitude1") is not None:
            userlon = request.form.get("longitude1") #type: string
            userlat = request.form.get("latitude1") #type: string
        else:
            userlon = request.form.get("longitude") #type: string
            userlat = request.form.get("latitude") #type: string
        radius = request.form.get("slider") #type: string

        try:
            radius, userlon, userlat = float(radius), float(userlon), float(userlat)
        except:
            return render_template('getyourlocation.html')
        else:
            
            d = { "lat":float(userlat), "lng":float(userlon) }
            jlis = import_json()
            jlis.append(d)
            export_json(jlis)
            coordinates_2_txt(userlon,userlat)

            allbusstops = stops.getbusstopdistance(commands["selectfromdatabase"], userlat=userlat, userlon=userlon, radius=radius)

            for busstop in allbusstops:
                for mrtbusstop in allmrtbusstops:
                    
                    if busstop['ServiceNo'] == mrtbusstop['ServiceNo'] and busstop['Direction'] == mrtbusstop['Direction']:
                        mrtstation, mrtline = stops.description_2_mrtname(mrtbusstop['Description'])

                        busstopcode = busstop['BusStopCode']
                        mrtbusstopcode = mrtbusstop['BusStopCode']
                        serviceno = busstop['ServiceNo']
                        direction = busstop['Direction']

                        startsequence = stops.findstopsequence(commands["findstopsequence"], direction=str(direction), serviceno=str(serviceno),busstopcode=str(busstopcode))

                        endsequence = stops.findstopsequence(commands["findstopsequence"], direction=str(direction), serviceno=str(serviceno),busstopcode=str(mrtbusstopcode))

                        numberofstops = abs(int(startsequence) - int(endsequence))
                        distance_metres_rounded = int(busstop['Distance']*1000)

                        dic = {
                            "mrt_station": mrtstation,
                            "mrt_line": mrtline,
                            "walkdistance": f"{distance_metres_rounded}m",
                            "board_busstopdescription": busstop['Description'].title(),
                            "busstopcode": busstopcode,
                            "busservice": serviceno,
                            "numberofstops": numberofstops,
                            "alight_busstopdescription": mrtbusstop['Description'].title(),
                            "busstoplat": busstop['BusStopLat'],
                            "busstoplon": busstop['BusStopLon']
                        }
                        data.append(dic)
                        
                    else:
                        pass
            return render_template('findabus.html', userlon = userlon, userlat = userlat, data=data, jsondata=json.loads(json.dumps(data)), mymap=mymap, radius=radius)
           

    else:
        return render_template('getyourlocation.html')


@app.route('/help', methods=['GET'])
def help():
    return render_template('help.html')


@app.route('/coordinates', methods=['GET'])
def coordinates():
    with open('txt/coordinates.txt', 'r') as f:
        data = f.readlines()
        data.pop(0)
    return render_template('coordinates.html', data=data)


if __name__ == '__main__':
    app.run("0.0.0.0")