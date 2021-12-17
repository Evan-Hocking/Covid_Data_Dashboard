# NAME
Uk Covid Dashboard

# Description
The modules provided hosts a web application to display covid statistics and relevant news articles. 

# MODULES
## covid_data_handler
Hosts the webapplication and manages the covid data
## covid_news_handling
Completes and filters a news api request
## time_conversions
Converts time from a digital format to second format

# FUNCTIONS
## covid_data_handler
**parse_csv_data**(filename)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Opens covid data file  in a pandas data structure  
**process_covid_csv_data**(covid_csv_data)   
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3 functions actions performed and returns the required data

1. Sums cases for the 7 most recent days, ignoring the first 2 entries as one has no data and the other incomplete data
2. Fetches most recent entry to the hospital cases column from database, iterating past blank entries
3. Fetches most recent entry to the deaths column from the database, iterating past blank entries 

**update_covid_data**()  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Function accesses the config data and utilises to initiate an api request in another function  
**covid_API_request**(location="Exeter", location_type="ltla")  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Function creates the parameters required for the api request. Having this seperate from the request removes repeat lines of code for national and local data  
**api_request**(api_filter, layout)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Completes covid api requests using given parameters
is separate from previous function due to the multiple api requests made returns data in a json format  
**covid_json_7_day_accumulator**(data)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Function calculates the number of cases in the past 7 days from the covid data provided ignores first entry to the data as it is incomplete  
**nation_death_and_hospital_counter**(data)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Function completes 2 actions
1. Fetches the most recent national death statistic from the data set
2. Fetches the most recent nation hospital case statistic from the data set 

**covid_data_updater**(local_data, nation_data)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Updates the global covid_data dictionary with new data  
**covid_data_handler**()  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Reads the data from the global variable and returns it  
**config_read**()  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Opens and reads config file returning it in a json format  
**add_news_article**(title, description)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Adds new articles to the global list of news articles  
**get_news**()  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Fetches new news articles and filters them for the required data to be fed to the add_news_article function   
**remove_article**(name)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Removes article with specified namer from the news article list  
**schedule_covid_updates**(update_interval, update_name)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Schedules an update passing the update data to the update_handler  
**add_updates**(title,content) 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Adds update to the global update list to be shown on the UI   
**update_handler**(update_data)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Reads the update data and acts upon the update parameters included, calling the functions for the required updates  
**update_request_handler**(update_data)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Reads the update data provided handles the request
1. Reading data
2. Calling scheduler
3. Formating UI message

**remove_update**(name)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Removes update from the global updates list therefore removing it from UI  
**hello**()  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Manages UI updates
1. Fetches config data for UI
2. Runs scheduler
3. Reads updates from application and acts upon
4. Modifies UI parameters   

**launch**()  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Calls the required functions at the initial launch of the program these are the functions not required on every web update cycle  

## covid_news_handling
**news_api_request**(covid_terms="Covid, COVID-19, coronavirus")  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Function fetches news data  
Fetches news data from the news api and converts them into
    a json format  
**update_news**()  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Function filters the news request for the required data  
Filters the news request for headlines and descriptions, saves them to a dictionary and returns dictionary  

## time_conversions
**minutes_to_seconds**( minutes: str ) -> int  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Converts minutes to seconds  
**hours_to_minutes**( hours: str ) -> int  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Converts hours to minutes  
**hhmm_to_seconds**( hhmm: str ) -> int  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Converts time from the format hh:mm to a seconds format  
**hhmmss_to_seconds**( hhmmss: str ) -> int  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Converts time from the format hh:mm:ss to a seconds format  
**time_till**(target_time)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Finds the time remaining until a specified time given in format hh:mm  