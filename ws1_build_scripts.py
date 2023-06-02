#!/usr/bin/python3

import sys
import json
import requests
import get_access_token

## Get the list of applications
with open('app_list.json', 'r') as app_list_file:
	app_list_data=app_list_file.read()
	
app_list = json.loads(app_list_data)

## Get the API server and access token
SERVER = get_access_token.server
ACCESS_TOKEN = get_access_token.access_token

## Script should be created by this user (a WS1 user)
USER = "YOUR USER NAME"

## Create the response/request header
HEADER = {
	"Authorization": "Bearer " + ACCESS_TOKEN,
	"Accept": "application/json;version=2",
	"Content-Type": "application/json"
}


## get my user uuid
request_url = "{}/api/system/users/search?username={}".format(SERVER, USER)
response = requests.get(request_url, headers=HEADER)
#print("status_code: {}".format(str(response.status_code)))
api_response = response.json()
# print the result all pretty like
# print(json.dumps(api_response, sort_keys=True, indent=4))
user_uuid = api_response["Users"][0]["Uuid"]
#print(user_uuid)

## get the UUID of OG SJMC
request_url = "{}/api/system/groups/search".format(SERVER)
parameters = {
	"name": "SJMC"
}
response = requests.get(request_url, headers=HEADER, params=parameters)
#print("status_code: {}".format(str(response.status_code)))
api_response = response.json()

# print the result all pretty like
#print(json.dumps(api_response, sort_keys=True, indent=4))

group_uuid = api_response["OrganizationGroups"][0]["Uuid"]

for app in app_list['applications']:
	# Check if script name already exists
	request_url = "{}/api/mdm/groups/{}/scripts".format(SERVER, group_uuid)
	parameters = {
		"expand": False,
		"name": "TEST - macOS - update " + app['Name']
	}
	response = requests.get(request_url, headers=HEADER, params=parameters)
	#print(request_url)
	#print("status_code: {}".format(str(response.status_code)))
	api_response = response.json()
	
	# print the result all pretty like
	# print(json.dumps(api_response, sort_keys=True, indent=4))
	if api_response["RecordCount"] == 0:
		# Read in the udpate file
		update_script = open('Installomator Scripts/App normal Auto-update.sh', 'r')
		update_script_data = update_script.read()
		update_script.close()	
		
		update_script_data = update_script_data.replace('##ITEM##', app['InstallomatorFragment'])
		update_script_data = update_script_data.replace('##APP_PATH##', app['AppPath'])
		
		# Write the file out again
		# update_script = 'WS1 Scripts/{}-update.sh'.format(app['Name'])
		# update_script_file = open(update_script, 'w')
		# update_script_file.write(update_script_data)
		# update_script_file.close()
		
		# 12, 1 internal server error
		# 10, 2 internal server error
		# 21, 3
		# 10, 3 - macOS Bash
		# 10, 4
		
		script_body = {
			"name": "TEST - macOS - update " + app['Name'],
			"description": "",
			"platform": 10, # APPLE_OSX
			"organization_group_uuid": group_uuid,
			"allowed_in_catalog": False,
			"script_data": update_script_data,
			"execution_context": 1,
			"timeout": 300,
			"script_type": 3, # BASH
			"created_by": user_uuid#,
			#"catalog_display": {
			#	"display_name": "Text value",
			#	"display_desc": "Text value",
			#	"use_default_icon": True,
			#	"pre_action_text": "Text value",
			#	"post_action_text": "Text value",
			#	"action_type": "Text value"
			#}
		}
		
		request_url = "{}/api/mdm/groups/{}/scripts".format(SERVER, group_uuid)
		response = requests.post(request_url, headers=HEADER, json=script_body)
		print(app)
		print(request_url)
		print("status_code: {}".format(str(response.status_code)))
		print(response.text)
		print(response.json())
		#api_response = response.json()
		
		# print the result all pretty like
		#print(json.dumps(api_response, sort_keys=True, indent=4))
		sys.exit()