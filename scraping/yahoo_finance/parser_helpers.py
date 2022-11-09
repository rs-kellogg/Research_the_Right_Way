#######################################
# Helper Functions to Download HTML Pages
#######################################

# libraries used
import os
import pandas as pd
import random
import csv
import bs4 as bs

#########################################
# retrive all the html files in a directory
def file_list_maker(dir_path):
	input_files = []
	for file in os.listdir(dir_path):
		if file.endswith(".html"):
			input_files.append(os.path.join(dir_path, file))
	return input_files


###########################################
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
# read in html file and convert to soup
def html_to_soup(fname):
	with open(fname) as fp:
		soup = bs.BeautifulSoup(fp, 'html.parser')
		return soup

# #########################################
# extract the required fields from the soup object
def get_object_list(soup):
	content_select_default = [None, 1]
	try:
		press = soup.find('div',{'id':"quoteNewsStream-0-Stream"})
		articles = press.findAll('div',{'class':"Cf"})
		if len(articles) > 2:
			content_select = [articles, 0]
			return content_select
		else:
			return content_select_default
	except:
		return content_select_default

###########################################
# get a data frame of file contents
def get_list_contents(object_list,fname):

	# empty lists:
	fnameList = []
	article_names = []
	article_sites = []

	for i in object_list:
		fnameList.append(fname)

		# titles
		try:
			title = i.find('h3', {'class': 'Mb(5px)'})
			title = title.text
			article_names.append(title)
		except:
			article_names.append("NA")

		# urls
		try:
			website = i.find('a', href=True)
			website = website['href']
			website = 'https://finance.yahoo.com' + str(website)
			article_sites.append(website)

		except:
			article_sites.append("NA")

	# create data frame
	article_df = pd.DataFrame({'file name': fnameList, 'title': article_names,'website': article_sites,})
	return article_df
 


###########################################
# save lists contents to output file
def save_list_contents(content_df, output_file):
	# determine if file exists
    file_exists = os.path.isfile(output_file)

    # create or append csv file
    if not file_exists:
        content_df.to_csv(output_file, index=False)    
    else: 
        content_df.to_csv(output_file, mode='a', header=False, index=False)



###########################################
# consecutive error kill switch engage
def error_kill_switch(content_error_counter):
    if content_error_counter > 3:
        print("4 consecutive input files did not contain the html data table you need. Check code")
        return "yes"
    else:
        return "no"

