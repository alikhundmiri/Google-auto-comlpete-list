import sys
import time
import requests
import urllib.parse
from datetime import datetime
from urllib.parse import urlencode
import xml.etree.ElementTree as ET

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

	time.sleep(1)

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


if __name__ == '__main__':
	string = "Hyderabadi Food"
	search_engine = "google"
	LONGSEARCH = True
	file_name = create_doc_file(search_engine, string, LONGSEARCH)
	main(search_engine, string, file_name, LONGSEARCH)
	

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