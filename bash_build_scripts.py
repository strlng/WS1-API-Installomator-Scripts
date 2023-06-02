#!/usr/bin/python3

import sys
import json

## Get the list of applications
with open('app_list.json', 'r') as app_list_file:
	app_list_data=app_list_file.read()
	
app_list = json.loads(app_list_data)

def create_script(template_script, output_script, app):
	# Read in the template_script file
	script = open(template_script, 'r')
	script_data = script.read()
	script.close()	
	
	script_data = script_data.replace('##ITEM##', app['InstallomatorFragment'])
	script_data = script_data.replace('##APP_PATH##', app['AppPath'])
	
	# Write the file out again
	script = output_script
	script_file = open(output_script, 'w')
	script_file.write(script_data)
	script_file.close()

if [ ! -d "WS1 Scripts/install" ]; then
	mkdir -p "WS1 Scripts/install"
fi

if [ ! -d "WS1 Scripts/ss" ]; then
	mkdir -p "WS1 Scripts/ss"
fi

if [ ! -d "WS1 Scripts/update" ]; then
	mkdir -p "WS1 Scripts/update"
fi

for app in app_list['applications']:
	create_script('Installomator Scripts/App normal SS.sh', 'WS1 Scripts/ss/{}-ss.sh'.format(app['Name']), app)
	create_script('Installomator Scripts/App normal Auto-install.sh', 'WS1 Scripts/install/{}-install.sh'.format(app['Name']), app)
	create_script('Installomator Scripts/App normal Auto-update.sh', 'WS1 Scripts/update/{}-update.sh'.format(app['Name']), app)
