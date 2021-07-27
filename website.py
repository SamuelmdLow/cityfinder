'''
Title: City Finder Website
Client: William Li
Author: Samuel Low
Date Created: 29/6/2021
'''

from flask import Flask, render_template, request
import main


filters = []

# SITE SETUP
app = Flask(__name__)
@app.route('/', methods=["POST","GET"])
def index():
    if request.method == "POST":
        if "remove" in request.form:
            print("Removed Filter!")
            delete = request.form["remove"]
            deletenum = delete[0:-2]
            deletenum = int(deletenum)
            filters.pop(deletenum)
        if "submit" in request.form:
            selection = request.form["selection"]
            low = request.form["low"]
            high = request.form["high"]

            for i in range(len(filters)):
                if int(filters[i][0]) == int(selection):
                    filters.pop(i)
                    print("Removed Irrelevant Filter!")
                    break

            filters.append([int(selection), int(low), int(high)])
            print("Added Filter!")
    eligible    = main.getEligibleCities(filters)
    display     = main.getDisplay(eligible)

    display_filters = main.getSpecifications(filters)
    countries   = display[0]
    cities      = display[1]

    return render_template('index.html',countries=countries, cities=cities, filters=display_filters)

@app.route("/city/<id>")
def city(id):
    city        = main.getCity(id)
    paragraph   = main.getCityInformation(city)
    TYPES = ["City", "Province/State", "Country", "Lowest Temperature (C°)", "Highest Temperature (C°)", "Average Temperature (C°)", "Latitude", "Longitude", "Population", "Top University ranking", "Code"]

    wiki = main.getWikipedia(city)
    pag     = wiki[0]
    image   = wiki[1]

    flag = main.getFlag(city)

    if city[6] != "None":
        LATITUDE    = city[6]
        LONGITUDE   = city[7]
    else:
        LATITUDE    = "None"
        LONGITUDE   = "None"

    return render_template('city.html',LONGITUDE=LONGITUDE, LATITUDE=LATITUDE, types=TYPES, city=city,wikipedia=pag, paragraph=paragraph, image=image, flag=flag)

if __name__ == "__main__":
    app.run(debug=True)
