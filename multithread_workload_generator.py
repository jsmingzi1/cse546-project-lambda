from boto3 import client as boto3_client
import os
import sys
import requests
import os
import argparse
import _thread
import time
import subprocess
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed

input_bucket = "lcm-project3-input-bucket"
output_bucket = "lcm-project3-output-bucket"
test_cases = "test_cases/"

def clear_input_bucket():
	global input_bucket
	s3 = boto3_client('s3')
	list_obj = s3.list_objects_v2(Bucket=input_bucket)
	try:
		for item in list_obj["Contents"]:
			key = item["Key"]
			s3.delete_object(Bucket=input_bucket, Key=key)
	except:
		print("Nothing to clear in input bucket")

def clear_output_bucket():
	global output_bucket
	s3 = boto3_client('s3')
	list_obj = s3.list_objects_v2(Bucket=output_bucket)
	try:
		for item in list_obj["Contents"]:
			key = item["Key"]
			s3.delete_object(Bucket=output_bucket, Key=key)
	except:
		print("Nothing to clear in output bucket")

def upload_to_input_bucket_s3(path_name):
	global input_bucket
	s3 = boto3_client('s3')
	path=path_name['path']
	name=path_name['name']
	s3.upload_file(path + name, input_bucket, name)
	print("uploaded to input bucket..  name: " + name)

def upload_files(test_case):	
	global input_bucket
	global output_bucket
	global test_cases
	
	
	# Directory of test case
	test_dir = test_cases + test_case + "/"
	
	# Iterate over each video
	# Upload to S3 input bucket
	filelist=[]
	for filename in os.listdir(test_dir):
		if filename.endswith(".mp4") or filename.endswith(".MP4"):
			#print("Uploading to input bucket..  name: " + str(filename)) 
			#upload_to_input_bucket_s3({'path':test_dir, 'name':filename})
			filelist.append({'path':test_dir, 'name':filename})
	with ThreadPoolExecutor(max_workers = 100) as executor:
		executor.map(upload_to_input_bucket_s3, filelist)
			


def workload_generator():
	
	print("Running Test Case 1")
	upload_files("test_case_1")

	print("Running Test Case 2")
	upload_files("test_case_2")
	

from datetime import datetime
now = datetime.now()
print("Begin Time:", now.strftime('%Y-%m-%d %H:%M:%S'))

clear_input_bucket()
clear_output_bucket()	
workload_generator()	

now = datetime.now()
print("End Time:", now.strftime('%Y-%m-%d %H:%M:%S'))
