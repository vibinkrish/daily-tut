#!/usr/bin/env python

import cmd
import locale
import os
import pprint
import shlex
import sys

PY3 = sys.version_info[0] == 3

if PY3:
    from io import StringIO
else:
    from StringIO import StringIO


def main():
	myclient = client.DropboxClient('hCBker0RJnoAAAAAAAAALAFL8BkpF9IhH3dEHzm_q5eNbV_j--vyFiQbSZ44sBQn')
	print(myclient.account_info())
	file_path = 'Jingu.mp4'
	bigFile = open(file_path, 'rb')
	size = os.path.getsize(file_path)
	chunk_size = 1024
	uploader = myclient.get_chunked_uploader(bigFile, size)
	print("uploading: ",size)
	try:
		upload = uploader.upload_chunked()
	except rest.ErrorResponse as e:
		print (rest.ErrorResponse)
	uploader.finish('/'+file_path)

