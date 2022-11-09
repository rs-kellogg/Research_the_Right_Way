##########################################
# Extract Data from Yahoo Finance Articles
##########################################

# libraries used
import os
import parser_helpers as ph # file for parsing functions
import argparse

#########################################

### Inputs ####
input_dirname_default = 'downloads'
output_dirname_default = 'results'
output_file_default = "yahoo_article_data.csv"
main_dir = os.getcwd()

parser = argparse.ArgumentParser()
parser.add_argument("--input_dirname", nargs='?', default=input_dirname_default) 
parser.add_argument("--output_dirname", nargs='?', default=output_dirname_default) 
parser.add_argument("--output_file", nargs='?', default=output_file_default) 
args = parser.parse_args()

input_dirname = args.input_dirname
output_dirname = args.output_dirname
output_file = args.output_file


#########################################
### To Run ####

def main():

	# directories
	input_dir = main_dir + "/" + input_dirname
	input_files = ph.file_list_maker(input_dir) # make file list
	outdir_path = ph.output_dir_move(output_dirname) # move to output directory
	output_file_path = outdir_path + "/" + output_file

	# initialize consecutive error counter
	content_error_counter = 0

	# loop through html files for contents
	for fname in input_files:
		# get data
		soup = ph.html_to_soup(fname) # get soup object
		content_select = ph.get_object_list(soup) # get articles or error 
		content_error = content_select[1] # article list does not exit
		if content_select[0] is None:
			pass
		else:
			content_df = ph.get_list_contents(content_select[0], fname) # get output dataframe
			ph.save_list_contents(content_df, output_file_path)# save ouptut data frame to csv

		# abort code after 5 consecutive errors
		content_error_counter = (content_error_counter * content_error) + content_error
		if ph.error_kill_switch(content_error_counter) == "yes":
			break
	print("ran to completion.")

if __name__ == "__main__":
    main()
#########################################
