#######################################
# Download Yahoo Finance Articles
#######################################

# libraries used
import time
import os
import harvest_helpers as hh
import argparse
import subprocess

#########################################

### Inputs ####
input_file_default = 'tickers.txt'
output_dir_default = 'downloads'
url_string_default = 'https://finance.yahoo.com/quote/'
progress_file_default = "yahoo_progress.csv"
main_dir = os.getcwd()

parser = argparse.ArgumentParser()
parser.add_argument("--input_file", nargs='?', default=input_file_default) 
parser.add_argument("--output_dir", nargs='?', default=output_dir_default) 
parser.add_argument("--url_string", nargs='?', default=url_string_default) 
parser.add_argument("--progress_file", nargs='?', default=progress_file_default) 
args = parser.parse_args()

input_file = args.input_file
output_dir = args.output_dir
url_string = args.url_string
progress_file = args.progress_file

#########################################
### To Run ####

def main():

    # create ticker list from input file or progress file
    progress_select = hh.progress_file_maker(input_file, progress_file, url_string)
    tickerList = progress_select[0]

    # initialize consecutive error counters
    page_error_counter = 0
    storage_error_counter = 0
    content_error_counter = 0

    #loop through tickers to access and save html for yahoo finance pages
    for tick in tickerList[0:5]: 
        outdir = hh.output_dir_move(output_dir) # create/change into output dir
        file_count_init = len(os.listdir(outdir)) # initial file count in output dir
        url = hh.url_maker(tick, url_string) # create page url
        time.sleep(hh.randomize_sleep()) # randomize sleep time

        # get page source data
        #source_select = hh.page_get_request(url) # source data list
        source_select = hh.page_get_selenium(url) # source data list
        source = source_select[0] # source content
        response_code = source_select[1] # source status code
        page_error = int(source_select[2]) # status code error (0 or 1)

        # save page
        hh.page_save(source, str(tick.strip()) + '.html') # save page
        storage_error = hh.storage_alert(file_count_init, outdir)# file storage error (0 or 1)
        os.chdir(main_dir) # change to main dir
        value_error = hh.data_exists_error(source) # sanity check for html element error (0 or 1)
        hh.progress_tracker(response_code, progress_select[1], tick, progress_file, value_error) # save progress file

        # abort code after 5 consecutive errors
        page_error_counter = (page_error_counter * page_error) + page_error
        storage_error_counter = (storage_error_counter * storage_error) + storage_error
        content_error_counter = (content_error_counter * value_error) + value_error
        content_error_counter = 4
        if hh.error_kill_switch(page_error_counter, storage_error_counter, content_error_counter) == "yes":
            p = subprocess.Popen("source email_me.sh", stdout=subprocess.PIPE, shell=True)
            break


if __name__ == "__main__":
    main()
#########################################
