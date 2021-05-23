import json
import time
import csv
import sqlite3
from math import radians, cos, sin, asin, sqrt

def coordinates_2_txt(userlon=None, userlat=None):
    '''
    stores user's coordiantes into a txt file for easy debugging
    '''
    with open("txt/coordinates.txt", 'a') as f:
        coordinates = f"({str(userlon)}, {str(userlat)})"
        f.write(coordinates)
        f.write("\n")

def export_json(data):
    if type(data) != list:
        print('please input data as a list of dictionaries')
    elif type(data) == list:
        with open('static/coordinates.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

def import_json():
    with open('static/coordinates.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def json_2_db(jsonfile=None, dbfile=None, create=None, insert=None):
    '''
    stores data from json file into database, creates if does not exist
    '''
    if type(jsonfile) is not str or type(dbfile) is not str or type(create) is not str or type(insert) is not str:
        print('Please input jsonfile & dbfile & create & insert as strings.')

    else:
        with open (jsonfile, 'r', encoding = "utf-8") as f:
            data = json.load(f)

        con = sqlite3.connect(dbfile)
        c = con.cursor()
        
        c.execute(create)

        # insertinto Bus Routes table
        if 'Bus_Routes' in self.insert:
            for d in data:
                c.execute(self.insert, (d['ServiceNo'], d['Direction'], d['StopSequence'], d['BusStopCode'], d['WD_FirstBus'], d['WD_LastBus'], d['SAT_FirstBus'], d['SAT_LastBus'], d['SUN_FirstBus'], d['SUN_LastBus']))

        # insertinto Bus Services table
        elif 'Bus_Services' in self.insert:
            for d in data:
                c.execute(self.insert, (d['ServiceNo'], d['Direction'], d['AM_Peak_Freq'], d['AM_Offpeak_Freq'], d['PM_Peak_Freq'], d['PM_Offpeak_Freq']))

        # insertinto Bus Stops table
        elif 'Bus_Stops' in self.insert:
            print('stops')
            for d in data:
                c.execute(self.insert, (d['BusStopCode'], d['Description'], d['Latitude'], d['Longitude']))

        con.commit()
        con.close()

def haversine(lat1,lon1,lat2,lon2):
    """
    Calculates the distance between 2 coordinates
    """
    #validate input
    if type(lat1) and type(lon1) and type(lat2) and type(lon2) is not float:
        print('Please input coordinates as float')

    else:
        #convert to radians
        lat1,lon1,lat2,lon2 = map(radians, (lat1,lon1,lat2,lon2))

        #haversine formula
        delta_lon = lon2 - lon1
        delta_lat = lat2 - lat1
        a = sin(delta_lat/2)**2 + cos(lat1) * cos(lat2) * sin(delta_lon/2)**2
        c = 2 * asin(sqrt(a)) 
        r = 6371 # Radius of earth in kilometers. Use 3956 for miles
        return c * r

def quickSort(array): 
    '''
    returns a sorted array
    '''
    if len(array) <= 1:
        return array
    else:
        pivot = array[-1]
        ltearray = [el for el in array[:-1] if el["Distance"] <= pivot['Distance']]
        gtarray = [el for el in array[:-1] if el['Distance'] > pivot['Distance']]
        ltearray = quickSort(ltearray)
        gtarray = quickSort(gtarray)
        return ltearray + [pivot] + gtarray

#--------------------------------------

class BusStops:
    def __init__(self):
        pass

    def description_2_mrtname(self, description=None):
        '''
        input description of mrt bus stop, returns mrt station and mrt line
        '''
        mrtnames = []
        if type(description) is not str:
            print("Please input description as a string.")
        else:
            with open("csv/stations.csv", "r", newline="") as f:            
                data = csv.DictReader(f)
                for dic in data:
                    mrtnames.append(dic)
            for mrt in mrtnames:
                if description == mrt['mrtbusstopdescription']:
                    return mrt['mrtstation'], mrt['mrtline']
                else:
                    pass

    def getbusstopdistance(self, command=None,userlon=None,userlat=None,radius=None):
        '''
        calculates the distance between each bus stop and user location, returns all bus stops within specified distance (in km) 
        '''
        if (type(command) is not str) or (type(userlon) is not float) or (type(userlat) is not float) or (type(radius) is not float):
            print('Please input command as a string, radius as float, and coordinates as floats.')
        else:
            allbusstops = []
            con = sqlite3.connect("database/main.db")
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute(command)
            rows = cur.fetchall()

            for busstop in rows:
                busstoplon = busstop['Longitude']
                busstoplat = busstop['Latitude']
                
                distance = haversine(lat1=userlat, lon1=userlon, lat2=busstoplat, lon2=busstoplon) #in kilometers
                if distance <= radius:

                    d = {
                        "BusStopCode": busstop['BusStopCode'],
                        "Distance": distance,
                        "Description": busstop['Description'],
                        "ServiceNo": busstop['ServiceNo'],
                        "Direction": busstop['Direction'],
                        "BusStopLat": busstoplat,
                        "BusStopLon": busstoplon
                    }
                    
                    allbusstops.append(d)
                else:
                    pass
            con.commit()
            con.close()
            return allbusstops

    def getmrtbusstops(self, command=None):
        '''
        find and returns all bus stops outside an mrt station
        '''
        if type(command) is not str:
            print("Please input command as a string.")
        else:
            allmrtbusstops = []
            con = sqlite3.connect("database/main.db")
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute(command)
            rows = cur.fetchall()

            for mrtbusstop in rows:
                if ('Stn' in mrtbusstop['Description']) or ('STN' in mrtbusstop['Description']) or ('stn' in mrtbusstop['Description']):
                    if ('Aft' in mrtbusstop['Description']) or ('Bef' in mrtbusstop['Description']) or ('AFT' in mrtbusstop['Description']) or ('BEF' in mrtbusstop['Description']) or ('aft' in mrtbusstop['Description']) or ('bef' in mrtbusstop['Description']) or ('Police' in mrtbusstop['Description']) or ('PUB' in mrtbusstop['Description']) or ('Instn' in mrtbusstop['Description']) or ('Railway' in mrtbusstop['Description']) or ('Power' in mrtbusstop['Description']) or ('SPC' in mrtbusstop['Description']) or ('Sq/Bef' in mrtbusstop['Description']) or ('Fire' in mrtbusstop['Description']):
                        pass
                    else:
                        d = {
                            "BusStopCode": mrtbusstop['BusStopCode'],
                            "Description": mrtbusstop['Description'],
                            "ServiceNo": mrtbusstop['ServiceNo'],
                            "Direction": mrtbusstop['Direction']
                        }
                        allmrtbusstops.append(d)
                else:
                    pass
            con.commit()
            con.close()
            return allmrtbusstops

    def findstopsequence(self,command=None,serviceno=None,direction=None,busstopcode=None):
        '''
        returns the bus stop number of a bus service in its route given its direction
        '''
        if type(command) is not str or type(serviceno) is not str or type(direction) is not str or type(busstopcode) is not str:
            print("Please input all inputs as a string.")
        else:
            con = sqlite3.connect("database/main.db")
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute(command, (serviceno,direction,busstopcode))
            row = cur.fetchone()
            return row['StopSequence']        

#--------------------------------------

class BusCompanies():
    def __init__(self, filename=None):
        '''
        opens and reads json file and stores the data in a variable
        '''
        if filename == None:
            print('Please input filename as a string')
        elif type(filename) == str:
            with open (filename, 'r', encoding = "utf-8") as f:
                data = json.load(f)
        else:
            print('Please input filename as a string')

    def getbusservices(self, company=None):
        '''
        returns a list of bus services a company operates
        '''
        if company == None:
            print('Please input a bus company name as a string')
        elif type(company) == str:
            services = []
            with open ("json/bus_services.json", 'r', encoding = "utf-8") as f:
                data = json.load(f)
            for d in data:
                if company == d['Operator']:
                    services.append(d['ServiceNo'])
                else:
                    pass
            return services
        else:
            print('Please input a bus company name as a string')

    def getcategories(self, company=None):
        '''
        returns a list of bus categories which company operates
        '''
        if company == None:
            print('Please input a bus company name as a string')
        elif type(company) == str:
            categories = []
            with open ("json/bus_services.json", 'r', encoding = "utf-8") as f:
                data = json.load(f)
            for d in data:
                if company == d['Operator']:
                    categories.append(d['Category'])
                else:
                    pass
            return categories
        else:
            print('Please input a bus company name as a string')
    
    def countcategories(self, categories=None):
        '''
        count and return the number of each category of bus a company operates
        '''
        if categories == None:
            print('Please input category as a list')
        elif type(categories) == list:
            counted = {
                "Trunk": categories.count("TRUNK"),
                "Express": categories.count("EXPRESS"),
                "Feeder": categories.count("FEEDER"),
                "Townlink": categories.count("TOWNLINK"),
                "Citylink": categories.count("CITYLINK"),
                "2-Tier Flat Fare": categories.count("2-TIER FLAT FARE"),
                "Industrial": categories.count("INDUSTRIAL"),
                "Night Rider": categories.count("NIGHT RIDER")
            }
            return counted
        else:
            print('Please input category as a list')

#-------------------------------------

if __name__ == "__main__":
    json_2_db()
    coordinates_2_txt()
    export_json()
    import_json()
    BusStops()
    BusCompanies()
    quickSort()
    haversine()

    # getbusservices()
    # getcategories()
    # countcategories()
    # getmrtbusstops()
    # getbusstopdistance()
    # description_2_mrtname()
    # findstopsequence()