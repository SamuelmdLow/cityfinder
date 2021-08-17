'''
Title: City Finder Website
Client: William Li
Author: Samuel Low
Date Created: 29/6/2021
'''

from flask import Flask, render_template, redirect, url_for
import main


FILTERS = []

# SITE SETUP
app = Flask(__name__)

@app.route('/', methods=["POST","GET"])
def index():

    return redirect(url_for('filter', id="0"))

@app.route('/filter/<id>', methods=["POST","GET"])
def filter(id):

    global FILTERS

    if id == "0":
        print("None")
        FILTERS = []
        CRITERIA   = []
    else:
        DECRYPTED   = main.decryptCode(id)
        CRITERIA    = DECRYPTED[0]
        FILTERS     = DECRYPTED[1]
        print(CRITERIA)
        print(FILTERS)

    ELIGIBLE = main.getEligibleCities(FILTERS)

    if not CRITERIA:
        DISPLAY = main.getDisplay(ELIGIBLE)
    else:
        DISPLAY = main.rankCities(ELIGIBLE, CRITERIA)

    DISPLAY_CRITERIA = main.getCriteria(CRITERIA)

    DISPLAY_FILTERS = main.getSpecifications(FILTERS)
    CATAGORIES = DISPLAY[0]
    CITIES = DISPLAY[1]

    print(FILTERS)

    return render_template('index.html', code=id, catagories=CATAGORIES, cities=CITIES, filters=DISPLAY_FILTERS, rankings=DISPLAY_CRITERIA,)

@app.route("/delete/<code>/<type>/<id>/")
def remove(code,type, id):
    id = int(id)
    if "RNK:" in code or "FLT:" in code :
        other = None
        code = code[4:len(code)]
    else:
        code = code.split("::")
        if type == "R":
            other = code[1]
            code = code[0]
        else:
            other = code[0]
            code = code[1]
    changed = code.split(":")
    changed.pop(id)
    changed = ":".join(changed)

    if other != None and changed != "":
        if type == "R":
            newcode = changed+"::"+other
        else:
            newcode = other+"::"+changed
    elif changed != "":
        if type == "R":
            newcode = "RNK:"+changed
        else:
            newcode = "FLT:"+changed
    elif other != None:
        if type == "F":
            newcode = "RNK:"+other
        else:
            newcode = "FLT:"+other
    else:
        newcode = "0"

    print("Removed Filter! New Code is " + newcode)
    return redirect(url_for('filter',id=newcode))

@app.route("/city/<id>")
def city(id):
    CITY        = main.getCity(id)  # get the city information list
    paragraph   = main.getCityInformation(CITY)     # infromation in the city list in paragraph form
    TYPES = ["City", "Province/State", "Country", "Lowest Temperature (C°)", "Highest Temperature (C°)", "Average Temperature (C°)", "Latitude", "Longitude", "Population", "Top University ranking", "Code"]

    WIKI = main.getWikipedia(CITY)
    PAGE    = WIKI[0]   # get wikipedia page
    MONTAGE = WIKI[1]   # get wikipeida's "montage" of the city

    FLAG = main.getFlag(CITY)   # get the url of the flag of the city's country

    # get the latitude and longitude of the city
    if CITY[6] != "None":
        LATITUDE    = CITY[6]
        LONGITUDE   = CITY[7]
    else:
        LATITUDE    = "None"
        LONGITUDE   = "None"

    return render_template('city.html',LONGITUDE=LONGITUDE, LATITUDE=LATITUDE, types=TYPES, city=CITY,wikipedia=PAGE, paragraph=paragraph, flag=FLAG, montage=MONTAGE)

# run the app
if __name__ == "__main__":
    app.run(debug=True)
