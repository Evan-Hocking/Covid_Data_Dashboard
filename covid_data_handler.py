'''
 Name:        covid_data_handler
 Purpose:     Hosts the webapplication and manages the covid data

 Author:      Evan Hocking

 Created:     02/11/2021
 Completed:   12/12/2021
'''
import json
import sched
import time
import logging
from flask import Flask
from flask import render_template
from flask import request
from uk_covid19 import Cov19API
import pandas
from time_conversions import time_till
from covid_news_handling import update_news


logging.basicConfig(filename="logfile.log",level=logging.DEBUG)
s = sched.scheduler(time.time, time.sleep)
app = Flask(__name__)
news = []
future_updates = []
covid_data = {}


def parse_csv_data(filename):
    '''
    opens covid data file  in a pandas data structure
    '''
    data = pandas.read_csv(filename, header=None)
    logging.info("csv read")
    return data


def process_covid_csv_data(read_data):
    '''
    3 functions actions performed and returns the required data

    1. sums cases for the 7 most recent days, ignoring the first 2 entries
        as one has no data and the other incomplete data

    2. fetches most recent entry to the hospital cases column from database,
        iterating past blank entries

    3. fetches most recent entry to the deaths column from the database,
        iterating past blank entries
    '''
    #1
    cases=0
    for acc in range(3, 10):
        cases += int(read_data.iloc[acc,6])
    #2
    for acc in range (1, len(read_data)+1):
        if str(read_data.iloc[acc,5]).isnumeric():
            hospital_cases = int(read_data.iloc[acc,5])
            break
    #3
    for acc in range (1, len(read_data)+1):
        if str(read_data.iloc[acc,4]).isnumeric():
            deaths = int(read_data.iloc[acc,4])
            break
    #return statistics calculated
    return cases, hospital_cases, deaths


def update_covid_data():
    '''
    function accesses the config data and utilises to initiate an api request in another function
    '''
    data = config_read()
    local_location = data["Location"]
    location_type = data["Location_type"]
    covid_API_request(local_location, location_type)
    logging.info("covid data updated")
    logging.debug(covid_data)


def covid_API_request(location="Exeter", location_type="ltla"):
    '''
    function creates the parameters required for the api request.
    having this seperate from the request removes repeat lines of code for national and local data

    '''
    local_filter = [f"areaType={location_type}", f"areaName={location}"]
    nation_filter = ["areaType=nation", "areaName=England"]

    layout = {
    "areaCode": "areaCode",
    "areaName": "areaName",
    "areaType": "areaType",
    "date": "date",
    "deaths": "cumDailyNsoDeathsByDeathDate",
    "hospitalCases": "hospitalCases",
    "newCasesBySpecimenDate": "newCasesBySpecimenDate"
    }

    local_data = api_request(local_filter, layout)
    nation_data = api_request(nation_filter, layout)
    covid_data_updater(local_data,nation_data)


def api_request(api_filter, layout):
    '''
    completes covid api requests using given parameters

    is separate from previous function due to the multiple api requests made
    returns data in a json format
    '''
    api = Cov19API(filters=api_filter, structure=layout)
    data = api.get_json()
    data = data["data"]
    logging.info("api request complete")
    logging.debug(data)
    return data


def covid_json_7_day_accumulator(data):
    '''
    function calculates the number of cases in the past 7 days from the covid data provided

    ignores first entry to the data as it is incomplete
    '''
    cases = 0
    for acc in range (1, 8):
        cases += (data[acc])["newCasesBySpecimenDate"]
    return cases


def nation_death_and_hospital_counter(data):
    '''
    function completes 2 actions

    1. fetches the most recent national death statistic from the data set

    2. fetches the most recent nation hospital case statistic from the data set
    '''
    #1
    for acc in range(0, len(data)):
        if (data[acc])["deaths"]:
            deaths = (data[acc])["deaths"]
            break
    #2
    for acc in range(0, len(data)):
        if (data[acc])["hospitalCases"]:
            hospital_cases = (data[acc])["hospitalCases"]
            break
    return deaths, hospital_cases


def covid_data_updater(local_data, nation_data):
    '''
    updates the global covid_data dictionary with new data
    '''
    local_cases = covid_json_7_day_accumulator(local_data)
    nation_cases = covid_json_7_day_accumulator(nation_data)
    deaths, hospital_cases = nation_death_and_hospital_counter(nation_data)
    covid_data.update({"local_cases":local_cases})
    covid_data.update({"nation_cases":nation_cases})
    covid_data.update({"deaths":deaths})
    covid_data.update({"hospital_cases":hospital_cases})


def covid_data_handler():
    '''
    reads the data from the global variable and returns it
    '''
    local_cases = covid_data["local_cases"]
    nation_cases = covid_data["nation_cases"]
    deaths = covid_data["deaths"]
    hospital_cases = covid_data["hospital_cases"]
    return local_cases, nation_cases, deaths, hospital_cases


def config_read():
    '''
    opens and reads config file returning it in a json format
    '''
    with open("config.json", encoding="latin-1") as config_file:
        config = json.load(config_file)
    logging.info("config read")
    return config


def add_news_article(title, description):
    '''
    adds new articles to the global list of news articles
    '''
    news.append({
        "title":title,
        "content":description
    })


def get_news():
    '''
    fetches new news articles and filters them for the required data to be fed to
    the add_news_article function
    '''
    articles = update_news()
    news.clear()
    for key in articles:
        content = articles[key]
        add_news_article(key, content)
    if not news:
        logging.error("No News Articles Found")


def remove_article(name):
    '''
    removes article with specified namer from the news article list
    '''
    for acc in range(0,len(news)):
        article = news[acc]
        if article["title"]==name:
            del news[acc]
            break
    logging.info("news removed")


def schedule_covid_updates(update_interval, update_name, update_data):
    '''
    schedules an update passing the update data to the update_handler
    '''
    if update_interval:
        update_time = time_till(update_interval)
    else:
        update_time = 0
    exec(remove_spaces(update_name) + f" = s.enter({update_time},1,update_handler, argument=update_data)")
    logging.info("Update Scheduled: " + update_data)



def add_updates(title,content):
    '''
    adds update to the global update list to be shown on the UI
    '''
    future_updates.append({
        "title":title,
        "content":content
    })


def update_handler(update_data):
    '''
    reads the update data and acts upon the update parameters included,
    calling the functions for the required updates
    '''
    update_name = update_data["request_name"]
    repeat = update_data["repeat"]
    data_update = update_data["data_update"]
    news_update = update_data["news_update"]
    remove_update(update_name)
    if data_update:
        update_covid_data()
    if news_update:
        get_news()
    if repeat:
        update_request_handler(update_data)


def update_request_handler(update_data):
    '''
    reads the update data provided handles the request

    1. reading data
    2. calling scheduler
    3. formating UI message
    '''
    #1
    update_name = update_data["request_name"]
    update_time = update_data["update_time"]
    repeat = update_data["repeat"]
    data_update = update_data["data_update"]
    news_update = update_data["news_update"]
    #2
    update_parameters=[update_data]
    schedule_covid_updates(update_time, update_name, update_parameters)
    #3
    update_info = ""
    if update_time != 0:
        update_info = update_time
    if repeat:
        update_info = update_info + ", Repeats"
    if data_update:
        update_info = update_info + ", Update Covid Data"
    if news_update:
        update_info = update_info + ", Update News"
    if update_info.startswith(", "):
        update_info = update_info[2:]
    add_updates(update_name, update_info)


def remove_update(name):
    '''
    removes update from the global updates list
    therefore removing it from UI
    '''
    for acc in range(0, len(future_updates)):
        update = future_updates[acc]
        if update["title"]==name:
            del future_updates[acc]
            break


@app.route("/index")
def hello():
    '''
    manages UI updates

    1. fetches config data for UI
    2. runs scheduler
    3. reads updates from application and acts upon
    4. modifies UI parameters
    '''
    #1
    data = config_read()
    local_location = data["Location"]
    local_cases, nation_cases, deaths, hospital_case =  covid_data_handler()
    #2
    s.run(blocking=False)
    #3
    delete_news = request.args.get("notif")
    if delete_news:
        remove_article(delete_news)
    delete_update = request.args.get("update_item")
    if delete_update:
        remove_update(delete_update)
    request_name = request.args.get("two")
    if request_name:
        update = {
            "request_name":request_name,
            "update_time":0,
            "repeat":False,
            "data_update":False,
            "news_update":False }
        update_time = request.args.get("update")
        if update_time:
            update.update({"update_time":update_time})
        repeat = request.args.get("repeat")
        if repeat:
            update.update({"repeat":True})
        data_update = request.args.get("covid-data")
        if data_update:
            update.update({"data_update":True})
        news_update = request.args.get("news")
        if news_update:
            update.update({"news_update":True})
        update_request_handler(update)
    #4
    return render_template("index.html",
        title = "Covid Updates",
        location = local_location,
        local_7day_infections = local_cases,
        nation_location = "England",
        national_7day_infections = nation_cases,
        hospital_cases = f"National Hospital Cases: {hospital_case}",
        deaths_total = f"National Total Deaths: {deaths}",
        news_articles = news,
        updates = future_updates,
        image="logo.png",
        favicon="/static/logo.ico"
        )

def remove_spaces(data):
    '''Removes Spaces from string'''
    return data.replace(" ","")

def launch():
    '''
    calls the required functions at the initial launch of the program
    these are the functions not required on every web update cycle
    '''
    get_news()
    update_covid_data()


launch()


if __name__ =="__main__":
    app.run()
