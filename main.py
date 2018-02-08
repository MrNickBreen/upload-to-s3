#!/usr/bin/env python
import boto3
from os import listdir
from os.path import isfile, join
import shutil
import sys

# TODO(nick): not sure why my steal-my-idea specific user does't work. 
#session = boto3.session.Session(profile_name='steal-my-idea')
session = boto3.session.Session()
s3 = session.resource('s3')


# bucket = s3.Bucket('stealmyidea')

# find all the files to upload
mypath = './files-to-upload'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

if onlyfiles == []:
	print "please put some files in the files-to-upload directory!"
	sys.exit()

print "Would you like to upload the following files to S3?"
print onlyfiles
confirmation = raw_input("Y for confirmation: ")

if confirmation.lower() != "y": 
	print "You did not respond with y, exiting. Nothing was uploaded"
	sys.exit()

# loop through all the files we found and upload them one by one
for file_name in onlyfiles:
	print "Starting to upload file: " + file_name
	local_file_path = join(mypath, file_name)
	# Directory Under which file should get upload
	path = 'podcast-episodes/' 
	s3_uploaded_file_path = join(path, file_name)
	s3.meta.client.upload_file(local_file_path, 'stealmyidea', s3_uploaded_file_path)

	# move the file to uploaded
	shutil.move(local_file_path, "./files-that-have-been-uploaded")
	print "Finished uploading file: " + file_name

print "Finished uploading all files! Have a great day"