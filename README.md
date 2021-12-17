# Name:
UK Covid Dashboard

# Introduction:
This program hosts a web application to display coronavirus statistics and news.
It's purpose is to provide up to date statistics to the user and the newest relevant news articles.
The system includes a update scheduler allowing for the data and news displayed to be updated at a specified interval, without the need for a system restart.

# Prerequisites:
- Written in Python 3.9
- Written on Windows 10

# Installation:
## Required Installations:

- sched - $ pip install sched
- flask - $ pip install flask
- UK covid API - $ pip install uk_covid19
- pandas - $ pip install pandas


## Additional Libraries used:
- json
- time
- logging
- requests
- datetime

## Included modules:
- covid_data_handler
- covid_news_handling
- time_conversions

# Running the project:
## Configuring the Project
To operate the system the user will first need to modify the file **config.json** adding their newsapi key and entering their desired local location.

To obtain a **newsapi** key navigate to the following webpage: https://newsapi.org/

To learn more of the compatible locations, information can be found in the covid api Developer's guide: https://coronavirus.data.gov.uk/details/developers-guide/main-api

## Launching the Project
Once the config file is modified and saved the application can be launched.
If using a compatible operating system to run the application simply launch the **run.bat** file and refresh the webpage that appears.
In the event this is incompatible with the chosen operating system, launch the file covid_data_handler.py as a flask application using the command line then navigate to 'http://127.0.0.1:5000/index' in your chosen web browser.

**Once open do not close the command line used to launch the program/opened by the batch file**

## Using the Project
**Dismissing News Articles**  
To dismiss a news article click the 'x' in the top right corner of the articles widget

**Scheduling a Covid Data Update**  
Select a time, enter a recognisable title for the update and check the "Update Covid Data" checkbox before clicking submit. The update shall occur at the specified time. 

**Scheduling a News Update**  
Select a time, enter a recognisable title for the update and check the "Update news articles" checkbox before clicking submit. The update shall occur at the specified time. 

**NOTE:** If the time selected is equivalent or before the current time the update shall take place the following day.

**NOTE:** Both updates can take place simultaneously.

**Scheduling a repeating update**  
When Scheduling one of the 2 previous updates, select the repeat checkbox. The update shall occur at the specified time each day.

**Dismissing Updates**  
To dismiss an update click the 'x' in the top right corner of the chosen updates widget. 


# Credits
**index.html** - written by Matt Collison and provided by the University of Exeter

**time_conversions.py** - portions written by the computer science department at the University of Exeter
# Licence
## Copyright &copy; [2021] [Evan Richard Hocking]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.