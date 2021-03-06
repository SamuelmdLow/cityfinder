# main.py

'''
Title: City Finder
Client: Willian Li
Author: Samuel Low
Date Created: 19/6/2021
'''

# ---LIBRARIES--- #
import pathlib
import wikipedia

# ---CREATE FULL CITY INFO CSV FILE---#
# INPUT
# read data from CSV files
def getData(FILENAME):
    '''
    extract data from file and process into 2D arrays
    :param FILENAME: (string)
    :return: (list)
    '''

    FILE = open(FILENAME, encoding="ISO-8859-1")    # open file
    RAW_DATA = FILE.readlines()     # separate the content of the file by lines
    FILE.close()    # close the file

    for i in range(len(RAW_DATA)):  # for each line in the original file
        RAW_DATA[i] = RAW_DATA[i][:-1]  # remove the last character (\n)
        RAW_DATA[i] = RAW_DATA[i].split(',')    # split the line by each comma (CSV)

    return RAW_DATA

# PROCESSING
# add the data from the climate csv file to the full city array
def addClimate(CLIMATE_LIST, FULL_LIST):
    '''
    Add the information from "climate.csv" to the full list of city information
    :param CLIMATE_LIST: (list) list containing climate information
    :param FULL_LIST: (list) full list of city information
    :return: (list) Updated list of city information
    '''

    global CITY_LIST    # List of all cities in the city information database

    CLIMATE_LIST.pop(0)     # Remove the header of the table

    CITY = None

    for item in CLIMATE_LIST:   # for each item in the CLIMATE_LIST array
        if CITY != item[3]:     # if a new city has been reached in the data
            if CITY != None:    # if this is not the first time in the for loop
                if MONTHS == 0:
                    AVERAGE = None
                else:
                    AVERAGE = round(SUM/MONTHS,1)   # calculate the average temperature

                # Convert the temperatures values to Celcius
                LOW     = convertToCelcius(LOW)
                HIGH    = convertToCelcius(HIGH)
                AVERAGE = convertToCelcius(AVERAGE)

                CITY_INFORMATION    = [CITY, STATE, COUNTRY, LOW, HIGH, AVERAGE, None, None, None, None]
                FULL_LIST.append(CITY_INFORMATION)  # Add the climate data to the list of city information
                if STATE != None:
                    CITY_LIST.append(CITY + "_" + STATE + "_" + COUNTRY)
                else:
                    CITY_LIST.append(CITY+"_"+COUNTRY)
            CITY    = item[3]
            if item[2] != "":
                STATE = item[2]
            else:
                STATE = None
            COUNTRY = item[1]

            if COUNTRY == "US":
                COUNTRY = "United States"

            LOW     = None
            HIGH    = None
            MONTHS  = 0
            SUM     = 0

        TEMPERATURE = float(item[7])
        if TEMPERATURE != -99.0:
            MONTHS  = MONTHS + 1
            SUM     = SUM + TEMPERATURE

            # remember the temperature as the highest if it is the highest so far
            if LOW  == None or LOW  > TEMPERATURE:
                LOW   = TEMPERATURE

            # remember the temperature as the lowest if it is the lowest so far
            if HIGH == None or HIGH < TEMPERATURE:
                HIGH  = TEMPERATURE

    return FULL_LIST

# add the data from the population and coordinates csv file to the full city array
def addPopCords(POP_CORDS_LIST, FULL_LIST):
    '''
    Add the information from "PopulationAndCords.csv" to the full list of City information
    :param POP_CORDS_LIST: (list) list containing information from "PopulationAndCords.csv"
    :param FULL_LIST: (list) combined list of City information
    :return: (list) updated combined list of city information
    '''

    global CITY_LIST

    POP_CORDS_LIST.pop(0)   # remover the header
    for item in POP_CORDS_LIST:
        CITY = item[1][1:-1]    # remove the quotes ("")
        try:
            POPULATION = int(item[9][1:-1])     # extract the population of a city
        except:
            POPULATION = None

        LATITUDE    = item[2][1:-1]     # extract the latitude
        LONGITUDE   = item[3][1:-1]     # extract the longitude
        PROVINCE    = item[7][1:-1]     # extract the province
        COUNTRY     = item[4][1:-1]     # extract the country
        CODEA   = CITY+"_"+COUNTRY
        CODE   = CITY+"_"+PROVINCE+"_"+COUNTRY

        if CODEA in CITY_LIST:
            CITY_LIST[CITY_LIST.index(CODEA)] = CODE

        if CODE in CITY_LIST:   # if the is already in the full city database

            # add population and coordinates information
            INDEX = CITY_LIST.index(CODE)
            FULL_LIST[INDEX][1] = PROVINCE
            FULL_LIST[INDEX][6] = LATITUDE
            FULL_LIST[INDEX][7] = LONGITUDE
            FULL_LIST[INDEX][8] = POPULATION
        else:

            # create the city information list with the population and coordinates information
            INFORMATION = [CITY, PROVINCE, COUNTRY, None, None, None, LATITUDE, LONGITUDE,POPULATION, None]

            # add the city information list to the full city database
            FULL_LIST.append(INFORMATION)
            CITY_LIST.append(CODE)

    return FULL_LIST

# add the data from the university ranking csv file to the full city array
def addUniversities(UNIVERSITY_LIST, FULL_LIST):
    '''
    Add the information from "CityUniversityRankings.csv" to the combined list of City information
    :param UNIVERSITY_LIST: (list) list containing information from "CityUniversityRankings.csv"
    :param FULL_LIST: (list) combined list of City information
    :return: (list) updated combined list of city information
    '''
    print("university started")
    global CITY_LIST

    rank = 916
    for UNI in reversed(UNIVERSITY_LIST):
        UNI = UNI[0]
        if UNI in CITY_LIST:     # if the city has been recorded for the full city database
            INDEX = CITY_LIST.index(UNI)     # locate the city in the list
            FULL_LIST[INDEX][9] = rank      # add the university ranking to the city's information list
        else:
            UNI = UNI.split("_")
            if len(UNI) == 3:
                worse = UNI[0]+"_"+UNI[2]
                i = 0
                for CITY in CITY_LIST:
                    CODE = CITY.split("_")
                    #print(CODE)
                    if len(CODE) == 3:
                        CODE = CODE[0] + "_" + CODE[2]
                        if worse == CODE:  # if the city has been recorded for the full city database
                            FULL_LIST[i][9] = rank  # add the university ranking to the city's information list
                    i = i + 1

        rank = rank - 1     # Count backwards so that higher ranks will overwrite lower ones

    return FULL_LIST

# add a unique code representing the city to the full city array
def addCode(FULL_LIST):
    '''
    Add the unique codes of each city to the city infromation list of each city
    :param FULL_LIST: (list) 2d list of all city information
    :return: (list) updated list of city information
    '''
    for i in range(len(FULL_LIST)):

        # set up the items of the unique code for the city
        CITY = FULL_LIST[i][0]
        while " " in CITY:
            CITY = CITY[0:CITY.index(" ")] + CITY[CITY.index(" ")+1:len(CITY)]
        if FULL_LIST[i][1] != None:
            PROV = FULL_LIST[i][1][0:3]
        else:
            PROV = ""
        if " " in FULL_LIST[i][2]:
            COUN = FULL_LIST[i][2][0]+FULL_LIST[i][2][FULL_LIST[i][2].index(" ")+1]
        else:
            COUN = FULL_LIST[i][2][0:3]

        # add the city code to the end of the city information list
        FULL_LIST[i].append(CITY+PROV+COUN)
    return FULL_LIST

# OUTPUT
# write the contents of the full city array to a CSV file
def createFullCityInfoCSVFile():
    '''
    Create a CSV file of the combined city information
    :return:
    '''

    global FULL_CITY_CSV
    global FULL_LIST

    SAVED_FILE = open(FULL_CITY_CSV, "w", encoding="utf-8") # open the database
    SAVED_FILE.write("CITY, PROVINCE/STATE, COUNTRY, LOW TEMP, HIGH TEMP, AVERAGE TEMP, LATITUDE, LONGITUDE, POPULATION, UNIVERSITY RANKING, CODE\n")

    for i in FULL_LIST:     # for each city in the in the list
        data = ""

        # connect the city information into a string separated by commas (CSV)
        for a in i:
            data = data + str(a) + ","
        data = data + "\n"  # end the string with a new line
        SAVED_FILE.write(data)  # write the string to the city information CSV file
    SAVED_FILE.close()  # close the database

# SUBROUTINES RELATED TO FILTERING CITIES
# convert the list of filters into a readable form for displaying
def getSpecifications(FILTERS):
    '''
    format the list of filters into something readable to display to the user
    :param FILTERS: (list) list of filters on the city data, added by the user
    :return: (list) list of filters in a readable format for displaying to the user
    '''
    DISP_FILTERS = []

    TYPES = ["City", "Province/State", "Country", "Lowest Temperature (C??)","Highest Temperature (C??)", "Average Temperature (C??)", "Latitude", "Longitude", "Population", "University ranking"]

    for item in FILTERS:
        if item[0] == 9: # if the filter is about university ranking

            # add sentence about university ranking to the list
            DISP_FILTERS.append(TYPES[item[0]] + " is in the top " + str(item[2]))
        else:

            # add a general sentence to the list
            DISP_FILTERS.append(TYPES[item[0]] + " is between " + str(item[1]) + " and " + str(item[2]))

    return DISP_FILTERS

# SUBROUTINES RELATED TO FILTERING CITIES
# convert the list of filters into a readable form for displaying
def getCriteria(CRITERIA):
    '''
    format the list of criteria into something readable to display to the user
    :param CRITERIA: (list) list of criteria for the city data, added by the user
    :return: (list) list of criteria in a readable format for displaying to the user
    '''
    DISP_CRITERIA = []

    TYPES = ["City", "Province/State", "Country", "lowest temperature","highest temperature", "average temperature", "latitude", "Longitude", "population", "university ranking"]

    for item in CRITERIA:
        if item[0] == 3 or item[0] == 4 or item[0] == 5:
            unit = " C?? "
        elif item[0] == 8:
            unit = " people "
        else:
            unit = " "
        # add sentence about each item in the criteria list
        DISP_CRITERIA.append("The ideal " + TYPES[item[0]] + " is " + str(item[1]) + unit + "(weighted at x" + str(item[2]) +")")

    return DISP_CRITERIA

# obtain the list of cities that meet the parameters of the filter
def getEligibleCities(SPECIFICATIONS):
    '''
    get the a list of eligible cities based on the user inputed filters on city data
    :param SPECIFICATIONS:
    :return: (list) list of cities that meet the filters set by the user
    '''
    global FULL_LIST

    ELIGIBLE_CITIES = []    # setup list of eligible cities
    for CITY in FULL_LIST:  # for each city in the list of cities
        ELIGIBLE = True     # assume the city is eligible
        for SPEC in SPECIFICATIONS:     # for each filter in the list of filters
            try:
                if CITY[SPEC[0]] != "None":
                    VALUE = float(CITY[SPEC[0]])
                    if SPEC[1] <= VALUE <= SPEC[2]:
                        pass
                    else:
                        ELIGIBLE = False    # if the city does not meet the filter, mark it as not eligible
                        break
                else:
                    ELIGIBLE = False    # if city has no information for the filtered information, mark it not eligible
                    break
            except:
                pass

        if ELIGIBLE == True:
            ELIGIBLE_CITIES.append(CITY)  # if city remains eligible, add it to the eligible list 0,2,-2 (city, country, id)
    return ELIGIBLE_CITIES

def decryptCode(CODE):
    '''
    Split the information in the url into two lists
    :param CODE: (string) the url information
    :return: (list) a list with two lists that represent the information in the url
    '''

    CRITERIA    = []    # list representing items in the ranking criteria
    FILTER      = []    # list representing the filters

    if "::" in CODE:    # this means there is both a ranking criteria and a filter in the url
        RAW = CODE.split("::")
        CRITERIA = decryptRaw(RAW[0].split(":"))    # Split the ranking criterias into their list
        FILTER   = decryptRaw(RAW[1].split(":"))    # Split the filters into their list
    else:
        RAW = CODE[4:len(CODE)]
        if "FLT:" in CODE:  # There is only a filter in the url
            FILTER      = decryptRaw( RAW.split(":") )  # Split the filters into their list
        else:   # There is only a ranking criteria in the url
            CRITERIA    = decryptRaw( RAW.split(":") )  # Split the ranking criterias into their list

    return [CRITERIA, FILTER]

def decryptRaw(RAW):
    '''
    Convert the string representing the list of filters or list of ranking criteria into a two dimensional array
    :param RAW: (string) string representing the list of filters or list of ranking criteria
    :return: (list) two dimensional list filters or ranking criteria
    '''

    CLEAN = []
    for i in RAW:
        NAME = i[0:2]
        if NAME == "LT":
            SELECTION = 3
        elif NAME == "HT":
            SELECTION = 4
        elif NAME == "AT":
            SELECTION = 5
        elif NAME == "PP":
            SELECTION = 8
        else:
            SELECTION = 9

        NUMBERS = i[2:len(i)]
        NUMBERS = NUMBERS.split("_")
        NUM1 = float(NUMBERS[0])
        NUM2 = float(NUMBERS[1])

        CLEAN.append([SELECTION, NUM1, NUM2])
    return CLEAN

# organize the cities into groups of countries for displaying
def getDisplay(ELIGIGBLE_CITIES):
    '''
    organize the list of eligible cities into groups of cities that share the same country
    :param ELIGIGBLE_CITIES: (list) list of the cities that meet the filters set by the user
    :return: (list) two dimensional array containing a list of counties and a list with the corresponding cities
    '''
    COUNTRIES   = []
    CITIES      = []

    for city in ELIGIGBLE_CITIES:   # for each city in the list of eligible cities
        if city[2] in COUNTRIES:    # if the loop has already encounterd this country
            CITIES[COUNTRIES.index(city[2])].append([city[0],city[-2]])  # add the city to a list in the CITY list at the same index as the country
        else:
            COUNTRIES.append(city[2])   # add the country to the end of the countries list
            CITIES.append([[city[0],city[-2]]])  # add the city into a list at the end of the cities list
    return [COUNTRIES, CITIES]

def rankCities(ELIGIBLE_CITIES, CRITERIA):
    '''
    Uses the ranking criteria to rank cities from closest to farthest from ideal
    :param ELIGIBLE_CITIES: (list) two dimensional list of eligible ciites and their information
    :param CRITERIA: (list) two dimensional list of ranking criteria
    :return: (list) list with two lists inside, one of labels for groups of cities, and another with the groups of cities and their codes
    '''

    CITIES_SCORES = []  # cities along with their scored differences from the ideal values
    for CITY in ELIGIBLE_CITIES:    # iterates through every city
        CITIES_SCORES.append([CITY[0], CITY[-2], 0])    # adds the city CITIES_SCORES list
        for ITEM in CRITERIA:   # iterate through th ranking criteria
            if CITY[ITEM[0]] != "None":  # check if the city has information on a value that is in the criteria
                # 1. Calculate the difference between the city and the ideal and the cities value
                # 2. Multiply the difference by the criteria's weighting
                # 3. Add this to the Cities total difference score
                CITIES_SCORES[-1][2] = CITIES_SCORES[-1][2] + (abs(float(CITY[ITEM[0]]) - ITEM[1]) * ITEM[2])
            else:
                # if the city does not have information on a value that is in the criteria, remove it
                CITIES_SCORES.pop(-1)
                break

    # order the cities from lowest difference score to highest difference score
    CITIES_SCORES.sort(key=getDistance)

    LOWER = 0   # Start of the grouping
    UPPER = 1   # End of the grouping
    MULTIPLIER = 2  # The number that the next group will multiply in size by
    BOUNDARIES = []     # List of group labels ("top 1 to 5", etc)
    CITIES = []     # list of cities

    # Create groupings until they out grow the amount of cities
    while UPPER < len(CITIES_SCORES):
        if UPPER != 1:
            LOWER = UPPER   # start the group at the end of the old group

        # alternate between growing by 2x and 5x (5, 10, 50, 100, 500, etc...)
        if MULTIPLIER == 2:
            MULTIPLIER = 5
        else:
            MULTIPLIER = 2

        UPPER = UPPER * MULTIPLIER  # define the end of the group

        BOUNDARIES.append("Top " + str(LOWER + 1) + " to " + str(UPPER))    # Add the label to the BOUNDARIES list
        CITIES.append(CITIES_SCORES[LOWER:UPPER])   # Add the group of cities within the boundaries to the list of cities
    return [BOUNDARIES,CITIES]

def getDistance(CITY):
    DISTANCE = CITY[2]
    return DISTANCE

# locate the index of a city by it's ID
def getCity(CODE):
    '''
    obtain the city information list of a city using it's Code
    :param CODE: (str) unique Code which represents each city
    :return: (list) list of city information
    '''
    global FULL_LIST

    INLIST = False

    INDEX = 0

    # loop through the entire city list until the code matches
    for i in FULL_LIST:
        if i[-2] == CODE:
            # if the code matches, break from the loop and remember that the code is indeed in the city information list
            INLIST = True
            break
        INDEX = INDEX + 1

    # if the program remembers that the code was in the city information list
    if INLIST == True:
        print(FULL_LIST[INDEX])
        return FULL_LIST[INDEX]
    else:
        return None

# arrange the information from a city in the city array into a paragraph for displaying
def getCityInformation(CITYINFO):
    '''
    print the available information about a city to the user
    :param FULL_LIST: (list) combined list of City information
    :return: (str) paragraph on the city
    '''

    if CITYINFO != None:

        CITY        = CITYINFO[0]
        PROVINCE    = CITYINFO[1]
        COUNTRY     = CITYINFO[2]
        LOW         = CITYINFO[3]
        HIGH        = CITYINFO[4]
        AVERAGE     = CITYINFO[5]
        LATITUDE    = CITYINFO[6]
        LONGITUDE   = CITYINFO[7]
        POPULATION  = CITYINFO[8]
        UNIVERSITY  = CITYINFO[9]

        # add the suffix to the top university's rank
        if UNIVERSITY[-1] == "1":
            UNIVERSITY = UNIVERSITY + "st"
        elif UNIVERSITY[-1] == "2":
            UNIVERSITY = UNIVERSITY + "nd"
        else:
            UNIVERSITY = UNIVERSITY + "th"

        # add the geographic location of the city to the paragraph
        SENTENCE = "\n" + CITY + " is in "
        if PROVINCE != "None":
            SENTENCE = SENTENCE + PROVINCE + ", " + COUNTRY + ".\n"
        else:
            SENTENCE = SENTENCE + " " + COUNTRY + ".\n"

        # add the coordinates of the city to the paragraph
        if LATITUDE != "None":
            SENTENCE = SENTENCE + "The city's coordinates are latitude: " + LATITUDE + " , longitude: " + LONGITUDE + ".\n"

        # add the temperature information of the city to the paragraph
        if LOW != "None":
            SENTENCE = SENTENCE + "The temperature can get as low as " + LOW + " C and as high as " + HIGH + " C.\n"
            SENTENCE = SENTENCE + "The average yearly temperature is " + AVERAGE + " C.\n"

        # add the population of the city to the paragraph
        if POPULATION != "None":
            SENTENCE = SENTENCE + "There are around " + POPULATION + " people in the city.\n"

        # add the top university rank to the paragraph
        if UNIVERSITY[0:-2] != "None":
            SENTENCE = SENTENCE + "The city's top university is ranked " + UNIVERSITY + " in the world."

        return SENTENCE
    else:
        # error message
        return "Sorry! We have no information on this city."

# convert Fahrenheit (useless unit) to Celcius
def convertToCelcius(Fahrenheit):
    '''
    Conver fahrenheit to a better unit of measurement (celcius)
    :param Fahrenheit: (float) temperature in fahrenheit
    :return: (float) temperature in celcius
    '''

    CELCIUS = round(((Fahrenheit - 32) * 5) / 9, 1)     # fahrenheit to celcius conversion
    return CELCIUS

# get the wikipedia page and an image from the wikipedia page of a city
def getWikipedia(CITY):
    '''
    retrieve wikipedia page on the city and the first image in it
    :param city: (list) list of city information
    :return: (list) list containing the link to the wikipedia page and the link to the first image
    '''
    URL     = "None"
    MONTAGE = []

    # create the search query
    if CITY[0] == CITY[1] or CITY[1] == "None":
        QUERY = CITY[0] + ", " + CITY[2]
    else:
        QUERY = CITY[0]+", "+CITY[1]+" "+CITY[2]
    print("Query: " + QUERY)

    try:
        # search wikipedia with the search query
        RESULT = wikipedia.search(QUERY)

        TERMS = ["montage","at_night", "downtown", "skyline", "business", "hall", "aerial","bridge","stadium"," street","mount","lake"]
        if len(RESULT) > 0:     # if the search yielded results
            PAGE = wikipedia.page(RESULT[0])
            URL  = wikipedia.page(RESULT[0]).url    # get the top result's url
            if len(PAGE.images) > 0:
                for index in range(len(PAGE.images)):
                    x = PAGE.images[index].lower()

                    for TERM in TERMS:
                        if TERM in x:
                            MONTAGE.append(PAGE.images[index])
                            break
    except:
        pass
    print(MONTAGE)
    print(URL)
    return [URL,MONTAGE]

# get the flag of the country of a specific city
def getFlag(CITY):
    '''
    get the flag of the country of a city
    :param city: (list) city information list
    :return:
    '''
    try:
        COUNTRY = CITY[2].lower()
        if COUNTRY == "united states":  # united states has an exception as it is represented differently in the website
            FLAG = "https://cdn.countryflags.com/thumbs/united-states-of-america/flag-800.png"
        else:
            # replace any spaces in the country name with dashes
            while " " in COUNTRY:
                COUNTRY = COUNTRY[0:COUNTRY.index(" ")] + "-" + COUNTRY[COUNTRY.index(" ")+1:len(COUNTRY)]
            FLAG = "https://cdn.countryflags.com/thumbs/" + COUNTRY + "/flag-800.png"
    except:
        FLAG  = "None"
    print(FLAG)
    return FLAG

# VARIABLES

CLIMATE_CSV     = "Product/databases/climate.csv"
POP_CORDS_CSV   = "Product/databases/PopulationAndCords.csv"
FULL_CITY_CSV   = "Product/databases/fullCityInfo.csv"
UNIVERSITY_CSV  = "Product/databases/CityUniversityRankings.csv"

FULL_LIST   = []
CITY_LIST   = []

# Get Data
FIRST_RUN   =   True
if (pathlib.Path.cwd() / FULL_CITY_CSV).exists():
    FIRST_RUN   =   False

if FIRST_RUN == True:

    # Create a combined array of city information
    CLIMATE_LIST    = getData(CLIMATE_CSV)  # convert the climate.csv to a list
    POP_CORDS_LIST  = getData(POP_CORDS_CSV)    # convert the PopulationAndCords.csv to a list
    UNIVERSITY_LIST = getData(UNIVERSITY_CSV)   # convert the CityUniversityRankings.csv to a list
    FULL_LIST   = addClimate(CLIMATE_LIST, FULL_LIST)   # add data from CLIMATE_LIST list to the full city list
    del CLIMATE_LIST    # remove the CLIMATE_LIST list from memory
    FULL_LIST   = addPopCords(POP_CORDS_LIST, FULL_LIST)    # add data from POP_CORDS_LIST list to full city list
    del POP_CORDS_LIST  # remove the POP_CORDS_LIST list from memory
    FULL_LIST   = addUniversities(UNIVERSITY_LIST, FULL_LIST)   # add data from UNIVERSITY_LIST list to full city list
    del UNIVERSITY_LIST     # remove the UNIVERSITY_LIST list from memory
    FULL_LIST   = addCode(FULL_LIST)    # add the unique city code to each city
    createFullCityInfoCSVFile()     # Save the full city information list in CSV format
    # so that the data does not have to be compiled every time the website is run
else:
    # Get city information from the saved CSV file
    FULL_LIST = getData(FULL_CITY_CSV)  # convert the fullCityInfo.csv to a list
    FULL_LIST.pop(0)    # remove the header
