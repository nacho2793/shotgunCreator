import os, sys
import re
from shotgun_api3 import Shotgun
import pprint
import time
import os.path


print Shotgun

#sg = Shotgun("https://upgdl.shotgunstudio.com", login="ignacho", password="Minions2793" )
sg = Shotgun("https://upgdl.shotgunstudio.com", "NachoScript", "486c9aa2bf63e4a83f975e3928207342e15dfcfeb2066384d7e48f9da7087923" )

#Asking user:

"""Define: Asset or Shot"""
validation = False
typeToUpload = raw_input("What do you want to upload: Shoot o Asset? (S/A)\n").lower()
while validation==False:
	typeToUpload = typeToUpload.lower()
	if (typeToUpload=='s') or (typeToUpload=='a'):
		validation=True
		typeToUpload = 'Shot'
	elif typeToUpload=='a':
		validation=True
		typeToUpload = 'Asset'
	else:
		typeToUpload = raw_input("PLEASE, ENTER ONLY ONE LETTER OF THE OPTIONS\nWhat do you want to upload: Shoot o Asset? (S/A)\n")

"""Define the ID of Asset or Shot"""
validId = False
validRequest = False
ID = raw_input("Type the id of the %s:\n" % typeToUpload)
while validRequest==False:
	#Number Validation
	while validId==False:
		try:
			ID = int(ID)
			validId = True
		except:
			print "Invalid input, the id must be a Number"
			ID = raw_input("Type the CORRECT id of the Asset:\n")
	#Shotgun Validation
	try:
		shoot ={'id': ID, 'type': typeToUpload}
		filters = [['entity','is', shoot]]
		fields = ['code']
		versions = sg.find("Version", filters, fields)
		if len(versions)==0:
			print "The ID doesnt exist in Shotgun"
			ID = raw_input("Type the CORRECT id of the Asset:\n")
			validId= False
		else:
			print "The ID %s have this versions:\n" %ID
			for version in versions:
				print "  -%s" %version["code"]
			validRequest=True
	except:
		print "EXCEPTION:The ID doesnt exist in Shotgun"
		ID = raw_input("Type the CORRECT id of the Asset:\n")
"""Naming the Version"""
raw_name = raw_input("Enter a name for a version (without vXXX):\n")
final_name = ''
for version in versions:
	if raw_name.lower() in version["code"].lower():
		final_name = version["code"]
if final_name == '':
	final_name = raw_name+' v001'
	print ("Creating: %s\n" %final_name)
else:
	new_version = int(final_name[len(final_name)-3:])+1
	final_name = "%s%03d" %(final_name[:len(final_name)-3], new_version)
	print ("The new version created will be %s\n" % final_name)
description = raw_input("Type a description for your new version:\n")
create = False
file_path = raw_input("Add the path of the file to upload:\n")
while create==False:
	try:
		if os.path.isfile(file_path) :
			create=True
		else:
			file_path = raw_input("Add the CORRECT path of the file to upload:\n")
		
	except Exception as e:
		print e
		time.sleep(10)
data = {
'code': final_name,
'entity': {'id': ID, 'type':typeToUpload},
'description': description,
'sg_task': {'id': 2252 , 'type':'Task'},
'user': {'id':92, 'type': 'HumanUser'},
'sg_status_list': 'rev',
'project': {'id':110, 'type':'Project'}}
try:
	result = sg.create("Version", data)
#file_path = 'C:\\Users\\Nacho\\Pictures\\turtle.jpg'
	print sg.upload("Version", result["id"], file_path, field_name="sg_uploaded_movie", display_name="Media")
except Exception as e:
	print e
print "Version added Succesfully. Bye!"
time.sleep(15)
