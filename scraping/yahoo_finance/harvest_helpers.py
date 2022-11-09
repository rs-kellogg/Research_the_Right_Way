#######################################
# Helper Functions to Download HTML Pages
#######################################

# libraries used
import time
import requests
import os
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import random
import csv
import bs4 as bs
import json
import subprocess

# selenium
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
capabilities = DesiredCapabilities.CHROME.copy()
#capabilities['goog:loggingPrefs'] = {'performance': 'ALL'}
capabilities['loggingPrefs'] = { 'performance':'ALL' }


from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_experimental_option('w3c', False)
# chrome_options.add_argument("--headless") # Run selenium in headless mode




driver = webdriver.Chrome(ChromeDriverManager(path="/kellogg/proj/awc6034/drivers").install(), desired_capabilities=capabilities,options=chrome_options)
#driver = webdriver.Chrome(ChromeDriverManager().install(), desired_capabilities=capabilities,options=chrome_options)


#########################################
# make (possibly) and move into directory
def output_dir_move(dir_name):

    cwd = os.getcwd()
    out_dir = str(cwd) + "/" + str(dir_name)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    else:
        pass
    os.chdir(out_dir)
    return out_dir

#########################################
# create a url from tickers
def url_maker(input_str, url_string):  

    # select a video number from top 3
    input_str = input_str.strip()
    url = str(url_string) + str(input_str)
    return url

#########################################
# randomizes sleep times
def randomize_sleep(sleep_min=3, sleep_max=5):  

    sleep_time = random.randint(sleep_min, sleep_max)
    return sleep_time

#########################################
# GET request to page, 3 attempts or abort
def page_get_request(url):

    j = 0
    while True:
        j = j + 1
        time.sleep(5)
        source = requests.get(url, timeout=10)
        if source.status_code == 200:
            error_count = 0
            source_select = [source, source.status_code, error_count]
            return source_select
            break
        elif j > 2:
            error_count = 1
            source_select = [None, source.status_code, error_count]
            return source_select
            break

        time.sleep(60)
        print("It's sleeping!")


#########################################
# GET request to page, 3 attempts or abort
def page_get_selenium(url):

    j = 0
    while True:
        j = j + 1
        time.sleep(5)
        try:
            driver.set_page_load_timeout(60)
            driver.get(url)
        except TimeoutException as ex:
            print("Exception has been thrown. " + str(ex))
            error_count = 1
            source_select = [None, '', error_count]
        source = driver.page_source
        logs = driver.get_log('performance')
        status_code = get_status(logs)
        if status_code == 200:
            error_count = 0
            source_select = [source, status_code, 0]
            return source_select
            break
        elif j > 2:
            error_count = 1
            source_select = [None, status_code, error_count]
            return source_select
            break

        time.sleep(60)
        print("It's sleeping!")

# get status code
def get_status(logs):
    for log in logs:
        if log['message']:
            d = json.loads(log['message'])
            try:
                content_type = 'text/html' in d['message']['params']['response']['headers']['content-type']
                response_received = d['message']['method'] == 'Network.responseReceived'
                if content_type and response_received:
                    return d['message']['params']['response']['status']
            except:
                pass


#########################################
# save page source
def page_save(source, path):

    if source is not None:
        try:
            with open(path, "wb") as f:
                f.write(source.content)
        except:
            with open(path, 'w') as f:
                f.write(source)
        print("At " + time.strftime("%X") + ", we successfully saved " + str(path) + ".")

    else:
        print(str(path) + " did not successfully download.")


#########################################
# file storage alert
def storage_alert(file_count_init, outdir):
    file_count_new = len(os.listdir(outdir))
    if len(os.listdir(outdir)) - file_count_init != 1:
        print("New page was not successfully saved to file system.")
        return 1
    else:
        return 0

#########################################
# read in text files and save to empty list
def list_maker(input_file):

    if '.txt' in str(input_file):
        nameList = []
        with open(input_file, 'r') as f:
            for i in f:
                nameList.append(i.strip())
        return nameList
    else:
        print('input file is not a text file')
        return None



#########################################
# make progress file
def progress_file_maker(text_file, progress_file, url_string):


    file_exists = os.path.isfile(progress_file)
    if not file_exists:
        nameList = list_maker(text_file)
        urlList = []
        for i in nameList:
            url = url_maker(i, url_string)
            urlList.append(url)
        codeList = [None] * len(urlList)
        timeList = [None] * len(urlList)
        checkList = [None] * len(urlList)
        progress = pd.DataFrame(list(zip(nameList,urlList,codeList,timeList,checkList)), columns =['Entry', 'URLs', 'Response_Codes', 'Time_Stamps', 'Data_Check'])
        progress.to_csv(progress_file, index=False)

    else:
        progress = pd.read_csv(progress_file)
        run = progress[progress['Response_Codes'] != 200]
        nameList = run['Entry'].tolist()

    progress_select = [nameList, progress]
    return progress_select

#########################################
# track progress
def progress_tracker(response_code, progress_df, entry, progress_file, checked_value_error):

    progress_df['Response_Codes'][progress_df.Entry == entry] = response_code
    time_stamp = time.strftime("%X")
    progress_df['Time_Stamps'][progress_df.Entry == entry] = time_stamp
    check_exists = "yes" if checked_value_error == 0 else "no"
    progress_df['Data_Check'][progress_df.Entry == entry] = check_exists
    progress_df.to_csv(progress_file, index=False)

###########################################
# check if a table exists
def data_exists_error(source):
    if source is None:
        return 0
    else:
        try:
            soup = bs.BeautifulSoup(source.text, 'html.parser')
        except:
            soup = bs.BeautifulSoup(source, 'html.parser')
        try:
            press = soup.find('div',{'id':"quoteNewsStream-0-Stream"})
            articles = press.findAll('h3',{'class':"Mb(5px"})
            if len(articles) > 3:
                return 1
            else:
                return 0
        except:
            return 0

###########################################
# parsing starter (starts parsing after 10000 files are downloaded)
def parsing_starter(page_error, storage_error, download_counter, file_downloads = 10000):
    if page_error == 0 and storage_error == 0:
        download_counter = download_counter + 1
        print(download_counter)

    if download_counter > file_downloads:
        print("I started to parse.")
        p = subprocess.Popen("python 2_yahoo_parser.py", stdout=subprocess.PIPE, shell=True)
        download_counter = 0

    return download_counter



###########################################
# consecutive error kill switch engage
def error_kill_switch(page_error_counter, storage_error_counter, content_error_counter):
    if page_error_counter > 3:
        print("4 consecutive status code errors.  Check code")
        return "yes"
    elif storage_error_counter > 3:
        print("4 consecutive page files were not saved.  Contact Research Support about file storage issue.")
        return "yes"
    elif content_error_counter > 3:
        print("4 consecutive pages did not contain the html data you need. Check code")
        return "yes"
    else:
        return "no"





