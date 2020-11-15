import sys
import time
import requests
import urllib.parse
from datetime import datetime
from urllib.parse import urlencode
import xml.etree.ElementTree as ET
from collections import OrderedDict


keyword_list = []

keyword_found = 0

keyword_searched = 0

base_url = 'http://suggestqueries.google.com/complete/search'

# Updates
# 1. folder name for keyword
# 2. child folder for date
# 3. file for all keywords
# 4. CSV file for common keywords 
# 5. eliminate keywords with "tools" "hubspot" "jobs"
# 6. sort by search volume and keyword density


def create_doc_file(search, string, LONGSEARCH):
	print("\n-------LONG TAIL KEYWORD FINDER-------\n")
	print("Search Engine \t: ", search)
	print("Keyword \t: ", string)
	print("Long search \t: ", LONGSEARCH)
	print('\nCreating File...', end="")
	sys.stdout.flush()
	
	date_today = datetime.now().strftime("%d-%m-%Y")
	
	sub_folder = search
	if LONGSEARCH: string = string + ' [LONG]'

	file_name = (sub_folder + '/' + string + "_" + date_today).replace(' ', '-')+".txt"
	file = open(file_name, 'w+')

	print(' Created {}'.format(file_name))
	file.close()
	return file_name
	# file.write(keyword_list)

def write(keywords, file_name):
	# create a file and write
	# print(file_name)
	with open(file_name,"a+") as f:
		for keyword in keywords:
			f.write(keyword+"\n")


def string_search(file_name, search, string):
	# count how many keywords searched	
	global keyword_searched
	keyword_searched = keyword_searched + 1

	keywords = get_keywords(search, string)
	if keywords is not None:
		write(keywords, file_name)
		return len(keywords)
	else:
		return 0

def get_keywords(search_engine, string):
	# print("parsing {} now".format(string))

	
	# time.sleep(1)

	# OLD CODE
	# encord the string
	# encoded_string = urllib.parse.quote(string)
	# encoded_url = base_url + encoded_string
		
	# NEW CODE
	base_url = 'http://suggestqueries.google.com/complete/search'

	search_dictionary = {
	'output':'toolbar',
	'gl': 'in',
	'hl': 'en',
	'q' : string,
	}
	
	youtube_parameter = '&ds=yt'
	JSON_param = '&client=firefox'
	JSON_detail_param = '&client=chrome'


	if search_engine is 'youtube':
		search_dictionary['ds'] = 'yt'  
	
	# search_dictionary['client'] = 'chrome'

	encoded_url = base_url +'?'+ urlencode(search_dictionary)
	
	# print(encoded_url)

	# send a request
	r = requests.get(encoded_url)
	
	# read the request, and get all suggestions

	try:
		suggestions = ET.fromstring(r.content)
	except Exception as e:
		return None
	
	# try:
	# 	suggestions = ET.fromstring(r.content)
	# except xml.etree.ElementTree.ParseError:
	# 	pass

	# record all suggestions	
	keywords=[]
	this_keyword = 0
	for suggestion_ in suggestions.iter('suggestion'):
		# count how many keywords found
		global keyword_found
		keyword_found = keyword_found + 1
		keyword = suggestion_.attrib.get('data')
		keywords.append(keyword)
		this_keyword = this_keyword + 1

		# print(type(suggestion_.attrib.value()))
	return keywords

def main(search_engine, string, file_name, LONGSEARCH):
	# initial string
	print("Finding longtail {} keywords for '{}'... ".format(search_engine, string), end="")
	sys.stdout.flush()
	found_core_keyword = string_search(file_name, search_engine, string)
	print("Found {}".format(found_core_keyword))

	for i in range(ord('A'), ord('Z') + 1):
		print("Finding longtail {} keywords for '{}' with {}... ".format(search_engine, string, chr(i)), end = "")
		sys.stdout.flush()
		# prefixed alphabet
		found_core_keyword_in_loop = 0
		found_core_keyword_in_loop = found_core_keyword_in_loop + string_search(file_name, search_engine, chr(i)+" "+string)
		if LONGSEARCH: found_core_keyword_in_loop = found_core_keyword_in_loop + string_search(file_name, search_engine, chr(i)+chr(i)+" "+string)

		# postfixed alphabet
		found_core_keyword_in_loop = found_core_keyword_in_loop + string_search(file_name, search_engine, string+" "+chr(i))
		if LONGSEARCH: found_core_keyword_in_loop = found_core_keyword_in_loop + string_search(file_name, search_engine, string+" "+chr(i)+chr(i))
		
		print("Found {}".format(found_core_keyword_in_loop))

	print("---REPORT---")
	print('Found {} keywords by searching {} keywords on {}\n'.format(keyword_found, keyword_searched, search_engine))


def common_keywords(file_name, string):
	
	# list of new keywords
	with open(file_name,"r") as f:
		keywords = f.readlines()
	keywords = [x.strip() for x in keywords]
	

	# original keyword, string. Split by words
	string_words = string.lower().split()
	# stop_words = ['on','of','the','if','it','a','an']
	
	print("\n-------Word Repeating Frequently-------\n")


	
	print('cleaning keywords... ', end = "")
	sys.stdout.flush()

	sublist = []
	# This nested for loop is very complex. it turns keyword from ['this is a keyword'] to ['this','is','a','keyword']. 
	# and then it gives is [['this','is','a','keyword'],['those','are','also','keywords']]
	# and then if each of those sub keywords have any words from base keywords it excludes them from the new keyword list
	cleaned_keywords = [item for sublist in [keyword.split() for keyword in keywords] for item in sublist if item not in string_words]
	
	
	repeat_words = {i:cleaned_keywords.count(i) for i in cleaned_keywords}
	repeat_words = OrderedDict(sorted(repeat_words.viewitems(), key=lambda x: len(x[1])))

	print('DONE')

	for key, value in sorted (key_value.values()):
		print('{}\t{}'.format(value, key))

	print("\n--------------------------------------\n")
	F202 16-4-293 SSKPlaza Chanchalguda
if __name__ == '__main__':
	string = "How to win accounts"
	search_engine = "google"
	LONGSEARCH = True
	# file_name = create_doc_file(search_engine, string, LONGSEARCH)
	# main(search_engine, string, file_name, LONGSEARCH)

	file_name = 'google/how-to-win-accounts_13-10-2020.txt'
	common_keywords(file_name, string)
	

# 	print("Creating folders... ", end="")
# 	sys.stdout.flush()
# 	time.sleep(2) # fake process
# 	print("DONE")

# 	time.sleep(1)
	
# 	print("Creating files... ", end="")
# 	sys.stdout.flush()
# 	time.sleep(2) # fake process
# 	print("DONE")
# Add progress bar using: https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console