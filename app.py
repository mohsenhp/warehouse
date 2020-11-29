from flask import Flask, render_template, request, jsonify
from requests.exceptions import HTTPError
import requests
import json
import time

app = Flask(__name__)

def product_API_request(product):
	product_api = 'https://bad-api-assignment.reaktor.com/products/'
	try:
		response = requests.get(product_api + product)
		response.raise_for_status()
	except HTTPError as http_err:
		print (http_err)
	except NameError as e:
		print (e)
	
	# Returns a list of dictionaries like {'id': 'f33561de3a864f951a', 'type': 'jackets',... 'price': 52, 'manufacturer': 'reps'}
	return (response.json()) 


def availability_API_request(manufacturer):
	availability_api = 'https://bad-api-assignment.reaktor.com/availability/'
	try:
		response = requests.get(availability_api + manufacturer)
		response.raise_for_status()
	except HTTPError as http_err:
		return (http_err)
	except NameError as e:
		return (e)

    #Returns a list of dictionaries like {'id': 'F33561DE3A864F951A', 'DATAPAYLOAD':<INSTOCKVALUE>INSTOCK</INSTOCKVALUE>\n'}
	return (response.json()['response'])	

def show_data(product, index):
	i = index
	final_dict = {}
	availability_dict = {}
	manufacturer_list = list()
	product_dict = {}
	product_list = product_API_request(product)
	try:
		for item in product_list:
			if item['manufacturer'] not in manufacturer_list:
				manufacturer_list.append(item['manufacturer'])
			value_to_add = {'type': item["type"], 'name': item["name"], 'color': item["color"], 'price': item["price"], 'manufacturer': item["manufacturer"]}
			product_dict[(str(item["id"])).lower()] = value_to_add
	except NameError as e:
		return (e)
	if i not in range (len(manufacturer_list)):
		return ("There's an error in loading the data. Please try again.")
	availability_list = availability_API_request(manufacturer_list[i])
	try:
		for item in availability_list:
			key = (str(item['id'])).lower()
			value_to_add = str(item['DATAPAYLOAD'])
			availability_dict[key] = value_to_add

		for key1 in product_dict.keys():
		 	for key2 in availability_dict.keys():
		  		if key1 == key2:
		  			value_to_add = {'type': product_dict[key1]["type"], 'name': product_dict[key1]["name"], 'color': str(product_dict[key1]["color"]).replace("'", "").replace("]", "").replace("[", ""), 'price': product_dict[key1]["price"], 'manufacturer': product_dict[key1]["manufacturer"], 'availability': availability_dict[key2][len("<AVAILABILITY>\n  <INSTOCKVALUE>"):-len('</INSTOCKVALUE>\n</AVAILABILITY>')]}
		  			final_dict[key1] = value_to_add

		final_list = [(k, v) for k, v in final_dict.items()] 
	except NameError as e:
		return (e)

	return (final_list)


@app.route('/')
def home():
	return render_template("home.html")

@app.route('/jackets')
def jackets():
	if request.args:
		index = int(request.args.get('index'))
	else:
		index = 0
	final_list = show_data("jackets", index)
	return render_template("jackets.html", data = final_list)


@app.route('/shirts')
def shirts(): 
	if request.args:
		index = int(request.args.get('index'))
	else:
		index = 0
	final_list = show_data("shirts", index)
	return render_template("shirts.html", data = final_list)

@app.route('/accessories')
def accessories(): 
	if request.args:
		index = int(request.args.get('index'))
	else:
		index = 0
	final_list = show_data("accessories", index)
	return render_template("accessories.html", data = final_list)


if __name__ == '__main__':
	app.run(debug = True)