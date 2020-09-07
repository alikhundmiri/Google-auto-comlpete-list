
import time
import requests
import urllib.parse
from datetime import datetime
import xml.etree.ElementTree as ET

keyword_list = []


base_url = 'http://suggestqueries.google.com/complete/search?&output=toolbar&gl=us&hl=en&q='

def create_doc_file(string):
	print('creating file')
	# get date
	date_today = datetime.now().strftime("%d-%m-%Y")
	# add it to the string.
	file_name = (string + "_" + date_today).replace(' ', '-')+".txt"

	file = open(file_name, 'w+')
	print('created {}'.format(file_name))
	file.close()
	return file_name
	# file.write(keyword_list)

def write(keywords, file_name):
	# create a file and write
	# print(file_name)
	with open(file_name,"a+") as f:
		for keyword in keywords:
			f.write(keyword+"\n")

def main(string, file_name):
	# initial string
	# print(string)
	keywords = get_keywords(string)
	if keywords is not None: write(keywords, file_name)

	# prefixed alphabet
	for i in range(ord('A'), ord('Z') + 1):
		new_string = chr(i)+" "+string
		keywords = get_keywords(new_string)
		if keywords is not None: write(keywords, file_name)

	# postfixed alphabet
	for i in range(ord('A'), ord('Z') + 1):
		new_string = string+" "+chr(i)
		keywords = get_keywords(new_string)
		if keywords is not None: write(keywords, file_name)

def get_keywords(string):
	print("parsing {} now".format(string))
	time.sleep(2)
	# encord the string
	encoded_string = urllib.parse.quote(string)
	encoded_url = base_url + encoded_string
	
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

	for suggestion_ in suggestions.iter('suggestion'):
		keyword = suggestion_.attrib.get('data')
		keywords.append(keyword)
		
		# print(type(suggestion_.attrib.value()))
	return keywords




if __name__ == '__main__':
	string = "Covid test hyderabad"
	file_name = create_doc_file(string)

	main(string, file_name)




# start

# create file = date+keyword

# take keyword
# convert to url encoded
# search url
# grab all results
# add to file


